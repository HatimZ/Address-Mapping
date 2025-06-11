import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from src.history.service import HistoryService
from src.history.exceptions import HistoryError
from src.database.base import DatabaseClient


class MockDatabaseClient(DatabaseClient):
    async def save_query(self, query_data):
        return "test_id"

    async def get_history(self, limit):
        return [
            {
                "_id": "test_id",
                "kilometers": 10.5,
                "address1": "New York, NY",
                "address2": "Los Angeles, CA",
                "timestamp": datetime.utcnow().isoformat(),
            }
        ]

    async def get_total_queries(self):
        return 1


@pytest.fixture
def history_service():
    return HistoryService(MockDatabaseClient())


@pytest.mark.asyncio
async def test_get_history_success(history_service):
    result = await history_service.get_history(10)

    assert result.total == 1
    assert result.limit == 10
    assert len(result.queries) == 1
    assert result.queries[0].query_id == "test_id"
    assert result.queries[0].kilometers == 10.5
    assert result.queries[0].address1 == "New York, NY"
    assert result.queries[0].address2 == "Los Angeles, CA"


@pytest.mark.asyncio
async def test_get_history_database_error():
    class ErrorDatabaseClient(MockDatabaseClient):
        async def get_history(self, limit):
            raise Exception("Database error")

    service = HistoryService(ErrorDatabaseClient())

    with pytest.raises(HistoryError):
        await service.get_history(10)
