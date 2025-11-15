from pymongo import MongoClient
from typing import Optional
import config


class MongoDBConnection:
    def __init__(self, uri: str = config.MONGODB_URI):
        self.uri = uri
        self.client: Optional[MongoClient] = None
        
    def connect(self) -> MongoClient:
        if self.client is None:
            self.client = MongoClient(self.uri)
        return self.client
    
    def disconnect(self) -> None:
        if self.client:
            self.client.close()
            self.client = None
    
    def get_database(self, database_name: str):
        if self.client is None:
            self.connect()
        return self.client[database_name]
    
    def get_collection(self, database_name: str, collection_name: str):
        db = self.get_database(database_name)
        return db[collection_name]


def main():
    db_connection = MongoDBConnection()
    
    try:
        client = db_connection.connect()
        print("Connected to MongoDB successfully")
        
        db_names = client.list_database_names()
        print(f"Available databases: {db_names}")
        
        if db_names:
            db = db_connection.get_database(db_names[0])
            collections = db.list_collection_names()
            print(f"Collections in '{db_names[0]}': {collections}")
            
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
    finally:
        db_connection.disconnect()


if __name__ == "__main__":
    main()

