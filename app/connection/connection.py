from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class MongoDBConnection:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self.connect()

    def connect(self):
        """Establish connection to MongoDB"""
        try:
            # Get MongoDB URI from environment variables
            mongodb_uri = os.getenv('MONGODB_URI')
            if not mongodb_uri:
                raise ValueError("MONGODB_URI environment variable is not set")

            # Create MongoDB client
            self._client = MongoClient(mongodb_uri)
            
            # Get database name from environment variables
            db_name = os.getenv('MONGODB_DB_NAME')
            if not db_name:
                raise ValueError("MONGODB_DB_NAME environment variable is not set")
            
            # Get database instance
            self._db = self._client[db_name]
            
            # Test the connection
            self._client.admin.command('ping')
            print("Successfully connected to MongoDB!")
            
        except Exception as e:
            print(f"Error connecting to MongoDB: {str(e)}")
            raise

    def get_database(self):
        """Get database instance"""
        if self._db is None:
            self.connect()
        return self._db

    def get_collection(self, collection_name):
        """Get collection instance"""
        if self._db is None:
            self.connect()
        return self._db[collection_name]

    def close(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None 