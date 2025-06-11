from src.history.schemas import HistoryListResponse, HistoryResponse, PaginationInfo
from src.database.base import DatabaseClient
from typing import List
import math


class HistoryService:
    def __init__(self, database_client: DatabaseClient):
        self.database_client = database_client

    async def get_history(
        self, page: int = 1, page_size: int = 10
    ) -> HistoryListResponse:
        skip = (page - 1) * page_size

        total = await self.database_client.count()
        records = await self.database_client.find_many(
            skip=skip, limit=page_size, sort_by="timestamp", sort_order="desc"
        )

        total_pages = math.ceil(total / page_size)

        pagination = PaginationInfo(
            total=total, page=page, page_size=page_size, total_pages=total_pages
        )

        items = [
            HistoryResponse(
                query_id=str(record["_id"]),
                kilometers=record.get("kilometers"),
                miles=record.get("miles"),
                address1=record["address1"],
                address2=record["address2"],
                timestamp=record["timestamp"],
            )
            for record in records
        ]

        return HistoryListResponse(items=items, pagination=pagination)
