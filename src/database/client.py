from datetime import datetime
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from src.config import get_settings
from src.database.base import DatabaseClient
from src.database.exceptions import DatabaseError
from src.config import logger

settings = get_settings()


class MongoDBClient(DatabaseClient):
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client.address_distance
        self.collection = self.db.queries

    async def save_query(self, query_data: Dict[str, Any]) -> str:
        try:
            query_data["timestamp"] = datetime.utcnow()
            result = await self.collection.insert_one(query_data)
            logger.info(result)
            return str(result.inserted_id)
        except Exception as e:
            raise DatabaseError(f"Failed to save query: {str(e)}")

    async def get_history(self, limit: int) -> List[Dict[str, Any]]:
        try:
            cursor = self.collection.find().sort("timestamp", -1).limit(limit)
            results = await cursor.to_list(length=limit)
            return [
                {
                    **doc,
                    "_id": str(doc["_id"]),
                    "timestamp": doc["timestamp"].isoformat(),
                }
                for doc in results
            ]
        except Exception as e:
            raise DatabaseError(f"Failed to retrieve history: {str(e)}")

    async def get_total_queries(self) -> int:
        try:
            return await self.collection.count_documents({})
        except Exception as e:
            raise DatabaseError(f"Failed to get total queries: {str(e)}")
