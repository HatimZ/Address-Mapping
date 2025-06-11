from src.distance.service import DistanceService
from src.core.clients.geocoding.client import NominatimClient
from src.core.clients.database.mongodb import MongoDBClient


async def get_distance_service() -> DistanceService:
    geocoding_client = NominatimClient()
    database_client = MongoDBClient()
    return DistanceService(geocoding_client, database_client)
