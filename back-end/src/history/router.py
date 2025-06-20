from fastapi import APIRouter, Depends, Query, status, Request
from src.history.schemas import HistoryListResponse
from src.history.service import HistoryService
from src.history.dependencies import get_history_service
from src.core.security import SecurityService, limiter
from src.core.decorators.cache import cache_history_query

router = APIRouter(
    prefix="/history",
    tags=["Query History"],
    responses={
        400: {"description": "Invalid input"},
        500: {"description": "Internal server error"},
    },
)


@router.get(
    "",
    response_model=HistoryListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get distance calculation history",
    description="Retrieves a paginated list of previous distance calculations",
)
@limiter.limit("100/minute")
@cache_history_query
async def get_history(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of records per page"),
    service: HistoryService = Depends(get_history_service),
) -> HistoryListResponse:
    response = await service.get_history(page=page, page_size=page_size)
    return response
