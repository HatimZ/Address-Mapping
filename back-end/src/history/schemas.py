from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class HistoryResponse(BaseModel):
    query_id: str = Field(..., description="Unique identifier for the query")
    kilometers: Optional[float] = Field(
        None, description="Calculated distance in kilometers"
    )
    miles: Optional[float] = Field(None, description="Calculated distance in miles")
    address1: str = Field(..., description="First address used in calculation")
    address2: str = Field(..., description="Second address used in calculation")
    timestamp: datetime = Field(..., description="When the query was executed")


class PaginationInfo(BaseModel):
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of records per page")
    total_pages: int = Field(..., description="Total number of pages")


class HistoryListResponse(BaseModel):
    items: List[HistoryResponse] = Field(..., description="List of history records")
    pagination: PaginationInfo = Field(..., description="Pagination information")
