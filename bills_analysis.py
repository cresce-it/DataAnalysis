import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any
from main import MongoDBConnection
import config
import pytz


def get_week_start(date: datetime) -> datetime:
    days_since_monday = date.weekday()
    week_start = date - timedelta(days=days_since_monday)
    return week_start.replace(hour=0, minute=0, second=0, microsecond=0)


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
        "billing.annual_consumption.cost.previous_year_annual_cost": 1,
        "billing.annual_consumption.cost.from_date": 1,
        "billing.annual_consumption.cost.to_date": 1
    }
    
    cursor = collection.find(query, projection)
    data = list(cursor)
    
    return pd.DataFrame(data)


def is_email(value: str) -> bool:
    return isinstance(value, str) and "@" in value


def normalize_creator(created_by: str) -> str:
    if pd.isna(created_by) or created_by == "Unknown":
        return "agents"
    if is_email(created_by):
        return created_by
    return "agents"


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
    
    return df[['week_start', 'week_number', 'created_at', 'created_by', 'creator_normalized', 'vendor_name', 
               'bill_amount', 'annual_kwh', 'annual_cost']]


def aggregate_by_week(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    
    grouped = df.groupby(['week_start', 'week_number', 'vendor_name', 'created_by']).agg({
        'created_at': 'count',
        'bill_amount': 'sum',
        'annual_kwh': 'sum',
        'annual_cost': 'sum'
    }).reset_index()
    
    grouped.columns = ['week_start', 'week_number', 'vendor_name', 'created_by', 
                      'bills_count', 'total_bill_amount', 
                      'total_annual_kwh', 'total_annual_cost']
    
    grouped['avg_annual_cost_per_bill'] = grouped['total_annual_cost'] / grouped['bills_count']
    grouped['avg_bill_amount'] = grouped['total_bill_amount'] / grouped['bills_count']
    
    return grouped.sort_values('week_start', ascending=False)


def print_summary(df: pd.DataFrame, processed_df: pd.DataFrame) -> None:
    if df.empty:
        print("No bills found.")
        return
    
    print("\n" + "="*80)
    print("BILLS ANALYSIS BY WEEK")
    print("="*80)
    
    for week in df['week_start'].unique():
        week_data = df[df['week_start'] == week]
        week_number = week_data.iloc[0]['week_number'] if 'week_number' in week_data.columns else week.isocalendar()[1]
        week_total = week_data.groupby('week_start').agg({
            'bills_count': 'sum',
            'total_bill_amount': 'sum',
            'total_annual_kwh': 'sum',
            'total_annual_cost': 'sum'
        }).iloc[0]
        
        week_processed = processed_df[processed_df['week_start'] == week]
        creator_summary = week_processed.groupby('creator_normalized').agg({
            'created_at': 'count',
            'bill_amount': 'sum',
            'annual_kwh': 'sum',
            'annual_cost': 'sum'
        }).sort_values('created_at', ascending=False)
        
        print(f"\nWeek {week_number}")
        print("-" * 80)
        print(f"Total Bills: {int(week_total['bills_count'])}")
        print(f"Total Bill Amount: €{week_total['total_bill_amount']:,.2f}")
        print(f"Total Annual kWh: {week_total['total_annual_kwh']:,.0f} kWh")
        print(f"Total Annual Cost: €{week_total['total_annual_cost']:,.2f}")
        print(f"Average Annual Cost per Bill: €{week_total['total_annual_cost']/week_total['bills_count']:,.2f}")
        
        print("\nSummary by Creator:")
        for creator, row in creator_summary.iterrows():
            print(f"  {creator:<40} | Bills: {int(row['created_at']):<5} | "
                  f"€{row['bill_amount']:>10,.2f} | "
                  f"{row['annual_kwh']:>10,.0f} kWh | "
                  f"€{row['annual_cost']:>10,.2f}")
        
        print("\nBy Vendor and Creator:")
        for _, row in week_data.iterrows():
            print(f"  {row['vendor_name']:<30} | {row['created_by']:<30} | "
                  f"Bills: {int(row['bills_count']):<5} | "
                  f"€{row['total_bill_amount']:>10,.2f} | "
                  f"{row['total_annual_kwh']:>10,.0f} kWh | "
                  f"€{row['avg_annual_cost_per_bill']:>10,.2f}/bill")


def export_to_csv(df: pd.DataFrame, filename: str = "bills_analysis.csv") -> None:
    df.to_csv(filename, index=False)
    print(f"\nData exported to {filename}")


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
        
        print(f"Found {len(raw_df)} bills")
        
        print("Processing data...")
        processed_df = process_bills_data(raw_df)
        
        print("Aggregating by week...")
        aggregated_df = aggregate_by_week(processed_df)
        
        print_summary(aggregated_df, processed_df)
        
        export_to_csv(aggregated_df)
        
        print("\n" + "="*80)
        print("Analysis complete!")
        print("="*80)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        connection.disconnect()


if __name__ == "__main__":
    main()

