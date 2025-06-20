from motor.motor_asyncio import AsyncIOMotorClient
from src.config import get_settings
from src.core.clients.database.base import DatabaseClient
from typing import List, Dict, Any, Optional
from src.core.exceptions import DatabaseException
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class MongoDBClient(DatabaseClient):
    def __init__(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            self.db = self.client.address_distance
            self.collection = self.db.queries
        except Exception as e:
            raise DatabaseException(
                detail="Failed to initialize MongoDB connection", internal_error=str(e)
            )

    async def create(self, data: Dict[str, Any]) -> str:
        """Create a new record in MongoDB."""
        try:
            result = await self.collection.insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to create record: {str(e)}")
            raise DatabaseException(
                detail="Failed to create record", internal_error=str(e)
            )

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
            raise DatabaseException(
                detail="Failed to retrieve records", internal_error=str(e)
            )

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count total number of records."""
        try:
            query = filters or {}
            return await self.collection.count_documents(query)
        except Exception as e:
            logger.error(f"Failed to count records: {str(e)}")
            raise DatabaseException(
                detail="Failed to count records", internal_error=str(e)
            )

    async def close(self) -> None:
        """Close the MongoDB connection."""
        try:
            self.client.close()
        except Exception as e:
            logger.error(f"Failed to close MongoDB connection: {str(e)}")
            raise DatabaseException(
                detail="Failed to close database connection", internal_error=str(e)
            )
