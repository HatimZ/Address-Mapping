from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class HistoryResponse(BaseModel):
    query_id: str = Field(..., description="Unique identifier for the query")
    distance_km: float = Field(..., description="Calculated distance in kilometers")
    address1: str = Field(..., description="First address used in calculation")
    address2: str = Field(..., description="Second address used in calculation")
    timestamp: datetime = Field(..., description="When the query was executed")


class HistoryListResponse(BaseModel):
    queries: List[HistoryResponse] = Field(
        ..., description="List of historical queries"
    )
    total: int = Field(..., description="Total number of queries")
    limit: int = Field(..., description="Maximum number of queries returned")
