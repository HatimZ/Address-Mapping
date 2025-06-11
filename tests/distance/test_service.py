import pytest
from unittest.mock import AsyncMock, patch
from src.distance.service import DistanceService
from src.distance.exceptions import DistanceCalculationError
from src.geocoding.base import GeocodingClient
from src.database.base import DatabaseClient


class MockGeocodingClient(GeocodingClient):
    async def geocode(self, address: str):
        if address == "New York, NY":
            return {
                "latitude": 40.7128,
                "longitude": -74.0060,
                "address": "New York, NY, USA",
            }
        elif address == "Los Angeles, CA":
            return {
                "latitude": 34.0522,
                "longitude": -118.2437,
                "address": "Los Angeles, CA, USA",
            }
        raise Exception("Invalid address")


class MockDatabaseClient(DatabaseClient):
    async def save_query(self, query_data):
        return "test_id"

    async def get_history(self, limit):
        return []

    async def get_total_queries(self):
        return 0


@pytest.fixture
def distance_service():
    return DistanceService(MockGeocodingClient(), MockDatabaseClient())


@pytest.mark.asyncio
async def test_calculate_distance_success(distance_service):
    result = await distance_service.calculate_distance(
        "New York, NY", "Los Angeles, CA"
    )

    assert result.kilometers > 0
    assert result.query_id == "test_id"
    assert result.address1.address == "New York, NY, USA"
    assert result.address2.address == "Los Angeles, CA, USA"


@pytest.mark.asyncio
async def test_calculate_distance_geocoding_error(distance_service):
    with pytest.raises(DistanceCalculationError):
        await distance_service.calculate_distance("Invalid Address", "Los Angeles, CA")


@pytest.mark.asyncio
async def test_calculate_distance_database_error():
    class ErrorDatabaseClient(MockDatabaseClient):
        async def save_query(self, query_data):
            raise Exception("Database error")

    service = DistanceService(MockGeocodingClient(), ErrorDatabaseClient())

    with pytest.raises(DistanceCalculationError):
        await service.calculate_distance("New York, NY", "Los Angeles, CA")
