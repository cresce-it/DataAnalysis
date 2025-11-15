import pandas as pd
from main import MongoDBConnection
from typing import List, Dict, Any


def fetch_data_to_dataframe(
    connection: MongoDBConnection,
    database_name: str,
    collection_name: str,
    query: Dict[str, Any] = None,
    limit: int = None
) -> pd.DataFrame:
    collection = connection.get_collection(database_name, collection_name)
    
    cursor = collection.find(query or {})
    if limit:
        cursor = cursor.limit(limit)
    
    data = list(cursor)
    return pd.DataFrame(data)


def analyze_collection(
    connection: MongoDBConnection,
    database_name: str,
    collection_name: str
) -> None:
    df = fetch_data_to_dataframe(connection, database_name, collection_name)
    
    print(f"\nCollection: {collection_name}")
    print(f"Total documents: {len(df)}")
    print(f"\nDataFrame shape: {df.shape}")
    print(f"\nColumn names: {list(df.columns)}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nData types:")
    print(df.dtypes)
    print(f"\nBasic statistics:")
    print(df.describe())


if __name__ == "__main__":
    connection = MongoDBConnection()
    
    try:
        connection.connect()
        
        client = connection.client
        db_names = client.list_database_names()
        
        if db_names:
            db_name = db_names[0]
            db = connection.get_database(db_name)
            collections = db.list_collection_names()
            
            if collections:
                analyze_collection(connection, db_name, collections[0])
            else:
                print(f"No collections found in database '{db_name}'")
        else:
            print("No databases found")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.disconnect()

