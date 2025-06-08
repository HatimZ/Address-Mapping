import pytest
from src.geocoding.client import NominatimClient
from src.database.client import MongoDBClient
from src.distance.service import DistanceService
from src.history.service import HistoryService


@pytest.fixture
async def geocoding_client():
    return NominatimClient()


@pytest.fixture
async def database_client():
    return MongoDBClient()


@pytest.fixture
async def distance_service(geocoding_client, database_client):
    return DistanceService(geocoding_client, database_client)


@pytest.fixture
async def history_service(database_client):
    return HistoryService(database_client)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_distance_calculation_integration(distance_service):
    result = await distance_service.calculate_distance(
        "New York, NY", "Los Angeles, CA"
    )

    assert result.distance_km > 0
    assert result.query_id
    assert result.address1.address
    assert result.address2.address


@pytest.mark.integration
@pytest.mark.asyncio
async def test_history_integration(distance_service, history_service):
    # First calculate a distance
    distance_result = await distance_service.calculate_distance(
        "New York, NY", "Los Angeles, CA"
    )

    # Then check if it appears in history
    history_result = await history_service.get_history(10)

    assert history_result.total > 0
    assert any(
        query.query_id == distance_result.query_id for query in history_result.queries
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_geocoding_integration(geocoding_client):
    result = await geocoding_client.geocode("New York, NY")

    assert "latitude" in result
    assert "longitude" in result
    assert "address" in result
    assert isinstance(result["latitude"], float)
    assert isinstance(result["longitude"], float)
