import pandas as pd
from datetime import datetime, timedelta
from main import MongoDBConnection
import config
import requests
from typing import Optional


def get_week_start(date: datetime) -> datetime:
    days_since_monday = date.weekday()
    week_start = date - timedelta(days=days_since_monday)
    return week_start.replace(hour=0, minute=0, second=0, microsecond=0)


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
        "vendor_name": 1,
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
    df['week_start'] = df['created_at'].apply(get_week_start)
    df['week_number'] = df['week_start'].apply(lambda x: x.isocalendar()[1])
    
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
    
    df['vendor_name'] = df['vendor_name'].fillna('Unknown')
    df['created_by'] = df['created_by'].fillna('Unknown')
    df['creator_normalized'] = df['created_by'].apply(normalize_creator)
    
    return df[['week_start', 'week_number', 'created_by', 'creator_normalized', 'vendor_name',
               'bill_amount', 'annual_kwh', 'annual_cost']]


def get_week_stats(df: pd.DataFrame, week_start: datetime) -> dict:
    week_data = df[df['week_start'] == week_start]
    
    if week_data.empty:
        return {
            'bills_count': 0,
            'total_bill_amount': 0,
            'total_annual_kwh': 0,
            'total_annual_cost': 0,
            'avg_annual_cost_per_bill': 0
        }
    
    bills_count = len(week_data)
    total_bill_amount = week_data['bill_amount'].sum()
    total_annual_kwh = week_data['annual_kwh'].sum()
    total_annual_cost = week_data['annual_cost'].sum()
    avg_annual_cost_per_bill = total_annual_cost / bills_count if bills_count > 0 else 0
    
    creator_stats = week_data.groupby('creator_normalized').agg({
        'created_by': 'count',
        'bill_amount': 'sum',
        'annual_kwh': 'sum',
        'annual_cost': 'sum'
    }).sort_values('created_by', ascending=False)
    
    vendor_stats = week_data.groupby('vendor_name').agg({
        'created_by': 'count',
        'bill_amount': 'sum',
        'annual_kwh': 'sum',
        'annual_cost': 'sum'
    }).sort_values('created_by', ascending=False)
    
    return {
        'bills_count': bills_count,
        'total_bill_amount': total_bill_amount,
        'total_annual_kwh': total_annual_kwh,
        'total_annual_cost': total_annual_cost,
        'avg_annual_cost_per_bill': avg_annual_cost_per_bill,
        'creator_stats': creator_stats,
        'vendor_stats': vendor_stats
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


def generate_comparison_report(current_week: dict, last_week: dict, current_week_num: int, last_week_num: int) -> str:
    report = f"## 📊 Weekly Bills Comparison\n\n"
    report += f"**Week {current_week_num}** vs **Week {last_week_num}**\n\n"
    report += "---\n\n"
    
    report += "### Overall Metrics\n\n"
    
    bills_change = format_change(current_week['bills_count'], last_week['bills_count'])
    report += f"**Bills Added:** {current_week['bills_count']} (vs {last_week['bills_count']}) {bills_change}\n\n"
    
    amount_change = format_change(current_week['total_bill_amount'], last_week['total_bill_amount'])
    report += f"**Total Bill Amount:** €{current_week['total_bill_amount']:,.2f} (vs €{last_week['total_bill_amount']:,.2f}) {amount_change}\n\n"
    
    kwh_change = format_change(current_week['total_annual_kwh'], last_week['total_annual_kwh'])
    report += f"**Total Annual kWh:** {current_week['total_annual_kwh']:,.0f} kWh (vs {last_week['total_annual_kwh']:,.0f} kWh) {kwh_change}\n\n"
    
    cost_change = format_change(current_week['total_annual_cost'], last_week['total_annual_cost'])
    report += f"**Total Annual Cost:** €{current_week['total_annual_cost']:,.2f} (vs €{last_week['total_annual_cost']:,.2f}) {cost_change}\n\n"
    
    avg_cost_change = format_change(current_week['avg_annual_cost_per_bill'], last_week['avg_annual_cost_per_bill'])
    report += f"**Avg Annual Cost per Bill:** €{current_week['avg_annual_cost_per_bill']:,.2f} (vs €{last_week['avg_annual_cost_per_bill']:,.2f}) {avg_cost_change}\n\n"
    
    report += "---\n\n"
    report += "### Top Energy Providers This Week\n\n"
    
    if 'vendor_stats' in current_week and not current_week['vendor_stats'].empty:
        for vendor, row in current_week['vendor_stats'].head(3).iterrows():
            report += f"**{vendor}**\n"
            report += f"- Bills: {int(row['created_by'])}\n"
            report += f"- Bill Amount: €{row['bill_amount']:,.2f}\n"
            report += f"- Annual kWh: {row['annual_kwh']:,.0f} kWh\n"
            report += f"- Annual Cost: €{row['annual_cost']:,.2f}\n\n"
    
    report += "---\n\n"
    report += "### Top Contributors This Week\n\n"
    
    if 'creator_stats' in current_week and not current_week['creator_stats'].empty:
        for creator, row in current_week['creator_stats'].head(5).iterrows():
            report += f"**{creator}**\n"
            report += f"- Bills: {int(row['created_by'])}\n"
            report += f"- Bill Amount: €{row['bill_amount']:,.2f}\n"
            report += f"- Annual kWh: {row['annual_kwh']:,.0f} kWh\n"
            report += f"- Annual Cost: €{row['annual_cost']:,.2f}\n\n"
    
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
        current_week_start = get_week_start(today)
        last_week_start = current_week_start - timedelta(days=7)
        
        current_week_num = current_week_start.isocalendar()[1]
        last_week_num = last_week_start.isocalendar()[1]
        
        print(f"Analyzing Week {current_week_num} vs Week {last_week_num}...")
        
        current_week_stats = get_week_stats(processed_df, current_week_start)
        last_week_stats = get_week_stats(processed_df, last_week_start)
        
        report = generate_comparison_report(current_week_stats, last_week_stats, current_week_num, last_week_num)
        
        print("\n" + "="*80)
        print("WEEKLY COMPARISON REPORT")
        print("="*80)
        print(report)
        print("="*80)
        
        webhook_url = config.GLUE_WEBHOOK_URL
        target = config.GLUE_TARGET
        
        if not webhook_url:
            webhook_url = input("\nEnter Glue webhook URL (or press Enter to skip): ").strip()
        
        if webhook_url:
            if not target:
                target = input("Enter target (group ID or thread ID): ").strip()
            
            if target:
                print("\nSending to Glue...")
                if send_to_glue(webhook_url, target, report):
                    print("✅ Successfully sent to Glue!")
                else:
                    print("❌ Failed to send to Glue")
            else:
                print("No target provided, skipping webhook")
        else:
            print("No webhook URL provided, skipping webhook")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        connection.disconnect()


if __name__ == "__main__":
    main()

