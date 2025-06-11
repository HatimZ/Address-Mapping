import pytest
from httpx import AsyncClient
from src.main import app
from src.config import get_settings

settings = get_settings()


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_calculate_distance(client):
    response = await client.post(
        f"{settings.API_PREFIX}/distance/calculate",
        json={"address1": "New York, NY", "address2": "Los Angeles, CA"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "kilometers" in data
    assert "address1" in data
    assert "address2" in data
    assert "query_id" in data


@pytest.mark.asyncio
async def test_calculate_distance_invalid_input(client):
    response = await client.post(
        f"{settings.API_PREFIX}/distance/calculate",
        json={"address1": "", "address2": "Los Angeles, CA"},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_history(client):
    response = await client.get(f"{settings.API_PREFIX}/history")

    assert response.status_code == 200
    data = response.json()
    assert "queries" in data
    assert "total" in data
    assert "limit" in data


@pytest.mark.asyncio
async def test_get_history_with_limit(client):
    response = await client.get(f"{settings.API_PREFIX}/history?limit=5")

    assert response.status_code == 200
    data = response.json()
    assert len(data["queries"]) <= 5
