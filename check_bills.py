from main import MongoDBConnection
from collections import Counter

connection = MongoDBConnection()

try:
    connection.connect()
    collection = connection.get_collection("bills", "utility_bills")
    
    total_count = collection.count_documents({})
    print(f"Total bills in collection: {total_count}")
    
    status_counts = {}
    archived_counts = {}
    
    for doc in collection.find({}, {"status": 1, "is_archived": 1}):
        status = doc.get("status", "missing")
        archived = doc.get("is_archived", "missing")
        
        status_counts[status] = status_counts.get(status, 0) + 1
        archived_counts[archived] = archived_counts.get(archived, 0) + 1
    
    print("\nStatus distribution:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    
    print("\nArchived distribution:")
    for archived, count in sorted(archived_counts.items()):
        print(f"  {archived}: {count}")
    
    published_not_archived = collection.count_documents({
        "status": "published",
        "is_archived": False
    })
    print(f"\nBills with status='published' AND is_archived=False: {published_not_archived}")
    
    has_created_at = collection.count_documents({"created_at": {"$exists": True}})
    print(f"\nBills with created_at field: {has_created_at}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    connection.disconnect()

