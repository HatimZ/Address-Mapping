from motor.motor_asyncio import AsyncIOMotorClient
from src.config import get_settings
from src.database.base import DatabaseClient
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class MongoDBClient(DatabaseClient):
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client.address_distance
        self.collection = self.db.queries

    async def create(self, data: Dict[str, Any]) -> str:
        """Create a new record in MongoDB."""
        try:
            result = await self.collection.insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to create record: {str(e)}")
            raise

    async def find_many(
        self,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Find multiple records with pagination and sorting."""
        try:
            sort_direction = -1 if sort_order.lower() == "desc" else 1
            query = filters or {}

            cursor = self.collection.find(query)
            cursor = cursor.sort(sort_by, sort_direction)
            cursor = cursor.skip(skip).limit(limit)

            return await cursor.to_list(length=limit)
        except Exception as e:
            logger.error(f"Failed to find records: {str(e)}")
            raise

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count total number of records."""
        try:
            query = filters or {}
            return await self.collection.count_documents(query)
        except Exception as e:
            logger.error(f"Failed to count records: {str(e)}")
            raise

    async def close(self) -> None:
        """Close the MongoDB connection."""
        self.client.close()
