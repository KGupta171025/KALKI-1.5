from typing import Optional
from config.settings import settings

# Attempt to load Motor async driver, otherwise fallback to mock client
try:
    from motor.motor_asyncio import AsyncIOMotorClient
    motor_client = AsyncIOMotorClient(settings.MONGODB_URL)
    mongo_db = motor_client.get_default_database()
except ImportError:
    motor_client = None
    mongo_db = None

class MongoDBManager:
    """
    Abstractions for MongoDB document operations.
    """
    @staticmethod
    def get_database():
        if mongo_db is not None:
            return mongo_db
        # Fallback Mock for environments without installed motor packages
        class MockMongoCollection:
            async def insert_one(self, document: dict):
                return type('MockInsertResult', (object,), {"inserted_id": "mock-mongo-id"})()
            async def find_one(self, filter: dict):
                return {"_id": "mock-mongo-id", "document_name": "mock-spec-doc"}
            async def find(self, *args, **kwargs):
                class MockCursor:
                    async def to_list(self, length: int):
                        return []
                return MockCursor()
        class MockMongoDB:
            def __getitem__(self, name: str):
                return MockMongoCollection()
        return MockMongoDB()

mongo_manager = MongoDBManager()
