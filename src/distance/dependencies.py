from src.distance.service import DistanceService
from src.geocoding.client import NominatimClient
from src.database.client import MongoDBClient


async def get_distance_service() -> DistanceService:
    geocoding_client = NominatimClient()
    database_client = MongoDBClient()
    return DistanceService(geocoding_client, database_client)
