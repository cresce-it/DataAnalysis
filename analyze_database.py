from main import MongoDBConnection
from datetime import datetime, timedelta
import config
from collections import defaultdict


def get_week_start(date: datetime) -> datetime:
    days_since_monday = date.weekday()
    week_start = date - timedelta(days=days_since_monday)
    return week_start.replace(hour=0, minute=0, second=0, microsecond=0)


def analyze_collection(connection: MongoDBConnection, db_name: str, collection_name: str, week_start: datetime) -> dict:
    collection = connection.get_collection(db_name, collection_name)
    
    total_count = collection.count_documents({})
    
    week_query = {
        "$or": [
            {"created_at": {"$gte": week_start}},
            {"updated_at": {"$gte": week_start}},
            {"createdAt": {"$gte": week_start}},
            {"updatedAt": {"$gte": week_start}}
        ]
    }
    
    week_count = collection.count_documents(week_query)
    
    if week_count == 0:
        return None
    
    sample_doc = collection.find_one({})
    
    fields = {}
    if sample_doc:
        def extract_fields(doc, prefix=""):
            for key, value in doc.items():
                if key == "_id":
                    continue
                full_key = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    extract_fields(value, full_key)
                elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                    if len(value) > 0:
                        extract_fields(value[0], f"{full_key}[]")
                else:
                    field_type = type(value).__name__
                    if field_type == "ObjectId":
                        field_type = "ObjectId (reference)"
                    elif field_type == "datetime":
                        field_type = "datetime"
                    fields[full_key] = field_type
        extract_fields(sample_doc)
    
    indexes = list(collection.list_indexes())
    index_info = [{"name": idx.get("name"), "keys": idx.get("key")} for idx in indexes]
    
    return {
        "total_count": total_count,
        "week_count": week_count,
        "fields": fields,
        "indexes": index_info,
        "sample_keys": list(sample_doc.keys()) if sample_doc else []
    }


def main():
    connection = MongoDBConnection()
    
    try:
        print("Connecting to MongoDB...")
        connection.connect()
        client = connection.client
        
        week_start = get_week_start(datetime.now())
        
        print(f"\nAnalyzing databases for updates since {week_start.strftime('%Y-%m-%d')}...\n")
        
        db_names = client.list_database_names()
        
        findings = defaultdict(dict)
        
        for db_name in db_names:
            if db_name in ["admin", "local", "config"]:
                continue
            
            print(f"Analyzing database: {db_name}")
            db = connection.get_database(db_name)
            collections = db.list_collection_names()
            
            for collection_name in collections:
                print(f"  Checking collection: {collection_name}")
                result = analyze_collection(connection, db_name, collection_name, week_start)
                
                if result:
                    findings[db_name][collection_name] = result
                    print(f"    ✓ {result['week_count']} documents updated this week (total: {result['total_count']})")
        
        report = generate_report(findings, week_start)
        
        filename = f"{datetime.now().strftime('%Y%m%d')}data-analysis.md"
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"\n✓ Analysis complete! Report saved to {filename}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        connection.disconnect()


def generate_report(findings: dict, week_start: datetime) -> str:
    report = f"# MongoDB Database Analysis\n\n"
    report += f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += f"**Week Start:** {week_start.strftime('%Y-%m-%d')}\n\n"
    report += "---\n\n"
    
    if not findings:
        report += "## No Collections Updated This Week\n\n"
        report += "No collections found with updates since the week start date.\n"
        return report
    
    report += "## Summary\n\n"
    total_collections = sum(len(collections) for collections in findings.values())
    report += f"- **Databases with updates:** {len(findings)}\n"
    report += f"- **Collections with updates:** {total_collections}\n\n"
    
    report += "---\n\n"
    
    for db_name, collections in sorted(findings.items()):
        report += f"## Database: `{db_name}`\n\n"
        
        for collection_name, data in sorted(collections.items()):
            report += f"### Collection: `{collection_name}`\n\n"
            report += f"- **Total Documents:** {data['total_count']:,}\n"
            report += f"- **Updated This Week:** {data['week_count']:,}\n\n"
            
            if data['fields']:
                report += "#### Schema Fields\n\n"
                report += "| Field | Type |\n"
                report += "|-------|------|\n"
                for field, field_type in sorted(data['fields'].items()):
                    report += f"| `{field}` | {field_type} |\n"
                report += "\n"
            
            if data['indexes']:
                report += "#### Indexes\n\n"
                for idx in data['indexes']:
                    if idx['name'] != '_id_':
                        keys_str = ", ".join([f"`{k}` ({v})" for k, v in idx['keys'].items()])
                        report += f"- **{idx['name']}**: {keys_str}\n"
                report += "\n"
            
            report += "---\n\n"
    
    report += "## Recommendations for MCP Server\n\n"
    report += "### High Priority Collections\n\n"
    
    for db_name, collections in sorted(findings.items()):
        for collection_name, data in sorted(collections.items()):
            if data['week_count'] > 10:
                report += f"- **`{db_name}.{collection_name}`**: {data['week_count']} updates this week - High activity\n"
    
    report += "\n### Suggested MCP Tools\n\n"
    report += "Based on the collections analyzed, consider creating MCP tools for:\n\n"
    report += "1. **Query Tools**:\n"
    report += "   - Get document counts by date range\n"
    report += "   - Filter by common fields (status, type, vendor, etc.)\n"
    report += "   - Search by text fields\n\n"
    
    report += "2. **Aggregation Tools**:\n"
    report += "   - Sum numeric fields (amounts, kWh, costs)\n"
    report += "   - Group by categorical fields (vendor, creator, status)\n"
    report += "   - Calculate averages and totals\n\n"
    
    report += "3. **Comparison Tools**:\n"
    report += "   - Compare periods (this week vs last week)\n"
    report += "   - Compare by category (vendor, creator)\n"
    report += "   - Trend analysis\n\n"
    
    report += "4. **Pre-computed Queries**:\n"
    report += "   - Common date ranges (today, this week, this month)\n"
    report += "   - Common filters (active status, non-archived)\n"
    report += "   - Top N queries (top vendors, top creators)\n\n"
    
    return report


if __name__ == "__main__":
    main()

