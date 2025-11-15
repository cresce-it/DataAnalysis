import pandas as pd
from datetime import datetime, timedelta
from main import MongoDBConnection
import config
import requests
from typing import Optional


def get_day_start(date: datetime) -> datetime:
    return date.replace(hour=0, minute=0, second=0, microsecond=0)


def is_email(value: str) -> bool:
    return isinstance(value, str) and "@" in value


def normalize_creator(created_by: str) -> str:
    if pd.isna(created_by) or created_by == "Unknown":
        return "agents"
    if is_email(created_by):
        return created_by
    return "agents"


def fetch_bills(connection: MongoDBConnection) -> pd.DataFrame:
    collection = connection.get_collection("bills", "utility_bills")
    
    query = {
        "is_archived": False,
        "created_by": {"$nin": config.EXCLUDED_USER_IDS}
    }
    
    projection = {
        "created_at": 1,
        "created_by": 1,
        "billing.current_bill_consumption.total_amount": 1,
        "billing.annual_consumption.total": 1,
        "billing.annual_consumption.cost.previous_year_annual_cost": 1
    }
    
    cursor = collection.find(query, projection)
    data = list(cursor)
    
    return pd.DataFrame(data)


def process_bills_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    
    df = df.copy()
    
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['day_start'] = df['created_at'].apply(get_day_start)
    
    df['bill_amount'] = df['billing'].apply(
        lambda x: x.get('current_bill_consumption', {}).get('total_amount', 0) if isinstance(x, dict) else 0
    )
    
    df['annual_kwh'] = df['billing'].apply(
        lambda x: x.get('annual_consumption', {}).get('total', 0) if isinstance(x, dict) else 0
    )
    
    df['annual_cost'] = df['billing'].apply(
        lambda x: x.get('annual_consumption', {}).get('cost', {}).get('previous_year_annual_cost', 0) 
        if isinstance(x, dict) and isinstance(x.get('annual_consumption', {}), dict) 
        and isinstance(x.get('annual_consumption', {}).get('cost', {}), dict) else 0
    )
    
    return df[['day_start', 'bill_amount', 'annual_kwh', 'annual_cost']]


def get_day_stats(df: pd.DataFrame, day_start: datetime) -> dict:
    day_data = df[df['day_start'] == day_start]
    
    if day_data.empty:
        return {
            'bills_count': 0,
            'total_bill_amount': 0,
            'total_annual_kwh': 0,
            'total_annual_cost': 0,
            'avg_annual_cost_per_bill': 0
        }
    
    bills_count = len(day_data)
    total_bill_amount = day_data['bill_amount'].sum()
    total_annual_kwh = day_data['annual_kwh'].sum()
    total_annual_cost = day_data['annual_cost'].sum()
    avg_annual_cost_per_bill = total_annual_cost / bills_count if bills_count > 0 else 0
    
    return {
        'bills_count': bills_count,
        'total_bill_amount': total_bill_amount,
        'total_annual_kwh': total_annual_kwh,
        'total_annual_cost': total_annual_cost,
        'avg_annual_cost_per_bill': avg_annual_cost_per_bill
    }


def format_change(current: float, previous: float, reverse: bool = False) -> str:
    if previous == 0:
        return "🟢 NEW" if current > 0 else "⚪"
    
    change = ((current - previous) / previous) * 100
    abs_change = abs(change)
    
    if abs_change < 0.01:
        return "⚪"
    
    if reverse:
        is_positive = change < 0
    else:
        is_positive = change > 0
    
    emoji = "🟢" if is_positive else "🔴"
    sign = "+" if change > 0 else ""
    return f"{emoji} {sign}{change:.1f}%"


def generate_daily_report(today_stats: dict, last_week_stats: dict, today: datetime, last_week: datetime) -> str:
    report = f"## 📊 Daily Bills Report\n\n"
    report += f"**{today.strftime('%Y-%m-%d')}** vs **{last_week.strftime('%Y-%m-%d')}** (same day last week)\n\n"
    report += "---\n\n"
    report += "### Overall Metrics\n\n"
    
    bills_change = format_change(today_stats['bills_count'], last_week_stats['bills_count'])
    report += f"**Bills Added:** {today_stats['bills_count']} (vs {last_week_stats['bills_count']}) {bills_change}\n\n"
    
    amount_change = format_change(today_stats['total_bill_amount'], last_week_stats['total_bill_amount'])
    report += f"**Total Bill Amount:** €{today_stats['total_bill_amount']:,.2f} (vs €{last_week_stats['total_bill_amount']:,.2f}) {amount_change}\n\n"
    
    kwh_change = format_change(today_stats['total_annual_kwh'], last_week_stats['total_annual_kwh'])
    report += f"**Total Annual kWh:** {today_stats['total_annual_kwh']:,.0f} kWh (vs {last_week_stats['total_annual_kwh']:,.0f} kWh) {kwh_change}\n\n"
    
    cost_change = format_change(today_stats['total_annual_cost'], last_week_stats['total_annual_cost'])
    report += f"**Total Annual Cost:** €{today_stats['total_annual_cost']:,.2f} (vs €{last_week_stats['total_annual_cost']:,.2f}) {cost_change}\n\n"
    
    avg_cost_change = format_change(today_stats['avg_annual_cost_per_bill'], last_week_stats['avg_annual_cost_per_bill'])
    report += f"**Avg Annual Cost per Bill:** €{today_stats['avg_annual_cost_per_bill']:,.2f} (vs €{last_week_stats['avg_annual_cost_per_bill']:,.2f}) {avg_cost_change}\n\n"
    
    return report


def send_to_glue(webhook_url: str, target: str, message: str) -> bool:
    try:
        response = requests.post(
            webhook_url,
            json={
                "target": target,
                "text": message
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error sending to Glue: {e}")
        return False


def main():
    connection = MongoDBConnection()
    
    try:
        print("Connecting to MongoDB...")
        connection.connect()
        
        print("Fetching bills data...")
        raw_df = fetch_bills(connection)
        
        if raw_df.empty:
            print("No bills found in the database.")
            return
        
        print("Processing data...")
        processed_df = process_bills_data(raw_df)
        
        today = datetime.now()
        today_start = get_day_start(today)
        last_week_start = today_start - timedelta(days=7)
        
        print(f"Analyzing {today_start.strftime('%Y-%m-%d')} vs {last_week_start.strftime('%Y-%m-%d')}...")
        
        today_stats = get_day_stats(processed_df, today_start)
        last_week_stats = get_day_stats(processed_df, last_week_start)
        
        report = generate_daily_report(today_stats, last_week_stats, today_start, last_week_start)
        
        print("\n" + "="*80)
        print("DAILY COMPARISON REPORT")
        print("="*80)
        print(report)
        print("="*80)
        
        webhook_url = config.GLUE_WEBHOOK_URL
        target = config.GLUE_TARGET
        
        if webhook_url and target:
            print("\nSending to Glue...")
            if send_to_glue(webhook_url, target, report):
                print("✅ Successfully sent to Glue!")
            else:
                print("❌ Failed to send to Glue")
        else:
            print("Webhook URL or target not configured, skipping webhook")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        connection.disconnect()


if __name__ == "__main__":
    main()

