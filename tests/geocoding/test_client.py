import pytest
from unittest.mock import patch, AsyncMock
from src.geocoding.client import NominatimClient
from src.geocoding.exceptions import GeocodingError


@pytest.fixture
def geocoding_client():
    return NominatimClient()


@pytest.mark.asyncio
async def test_successful_geocoding(geocoding_client):
    mock_response = AsyncMock()
    mock_response.json.return_value = [
        {"lat": "40.7128", "lon": "-74.0060", "display_name": "New York, NY, USA"}
    ]
    mock_response.raise_for_status = AsyncMock()

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        result = await geocoding_client.geocode("New York, NY")

        assert result["latitude"] == 40.7128
        assert result["longitude"] == -74.0060
        assert result["address"] == "New York, NY, USA"


@pytest.mark.asyncio
async def test_no_results(geocoding_client):
    mock_response = AsyncMock()
    mock_response.json.return_value = []
    mock_response.raise_for_status = AsyncMock()

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        with pytest.raises(GeocodingError, match="No results found"):
            await geocoding_client.geocode("Invalid Address")


@pytest.mark.asyncio
async def test_http_error(geocoding_client):
    with patch("httpx.AsyncClient.get", side_effect=Exception("HTTP Error")):
        with pytest.raises(GeocodingError, match="Geocoding service error"):
            await geocoding_client.geocode("New York, NY")
