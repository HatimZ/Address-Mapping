import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch
from src.database.client import MongoDBClient
from src.database.exceptions import DatabaseError


@pytest.fixture
def database_client():
    return MongoDBClient()


@pytest.mark.asyncio
async def test_save_query(database_client):
    mock_collection = AsyncMock()
    mock_collection.insert_one.return_value = AsyncMock(inserted_id="test_id")
    database_client.collection = mock_collection

    query_data = {
        "distance_km": 10.5,
        "address1": "New York, NY",
        "address2": "Los Angeles, CA",
    }

    result = await database_client.save_query(query_data)
    assert result == "test_id"
    assert mock_collection.insert_one.called


@pytest.mark.asyncio
async def test_get_history(database_client):
    mock_collection = AsyncMock()
    mock_cursor = AsyncMock()
    mock_cursor.to_list.return_value = [
        {
            "_id": "test_id",
            "distance_km": 10.5,
            "address1": "New York, NY",
            "address2": "Los Angeles, CA",
            "timestamp": datetime.utcnow(),
        }
    ]
    mock_collection.find.return_value = mock_cursor
    database_client.collection = mock_collection

    results = await database_client.get_history(10)
    assert len(results) == 1
    assert results[0]["_id"] == "test_id"
    assert "timestamp" in results[0]


@pytest.mark.asyncio
async def test_get_total_queries(database_client):
    mock_collection = AsyncMock()
    mock_collection.count_documents.return_value = 5
    database_client.collection = mock_collection

    total = await database_client.get_total_queries()
    assert total == 5


@pytest.mark.asyncio
async def test_save_query_error(database_client):
    mock_collection = AsyncMock()
    mock_collection.insert_one.side_effect = Exception("Database error")
    database_client.collection = mock_collection

    with pytest.raises(DatabaseError, match="Failed to save query"):
        await database_client.save_query({"test": "data"})
