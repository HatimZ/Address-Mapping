from src.distance.service import DistanceService
from src.core.clients.geocoding.client import NominatimClient
from src.core.clients.database.mongodb import MongoDBClient
from functools import lru_cache


@lru_cache()
def get_geocoding_client() -> NominatimClient:
    """Get cached geocoding client instance."""
    return NominatimClient()


@lru_cache()
def get_database_client() -> MongoDBClient:
    """Get cached database client instance."""
    return MongoDBClient()


async def get_distance_service() -> DistanceService:
    geocoding_client = get_geocoding_client()
    database_client = get_database_client()
    return DistanceService(geocoding_client, database_client)
