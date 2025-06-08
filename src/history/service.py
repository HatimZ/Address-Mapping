from src.history.schemas import HistoryListResponse, HistoryResponse
from src.database.base import DatabaseClient
from src.history.exceptions import HistoryError


class HistoryService:
    def __init__(self, database_client: DatabaseClient):
        self.database_client = database_client

    async def get_history(self, limit: int) -> HistoryListResponse:
        try:
            queries = await self.database_client.get_history(limit)
            total = await self.database_client.get_total_queries()

            return HistoryListResponse(
                queries=[
                    HistoryResponse(
                        query_id=query["_id"],
                        distance_km=query["distance_km"],
                        address1=query["address1"],
                        address2=query["address2"],
                        timestamp=query["timestamp"],
                    )
                    for query in queries
                ],
                total=total,
                limit=limit,
            )
        except Exception as e:
            raise HistoryError(f"Failed to retrieve history: {str(e)}")
