from fastapi import APIRouter, Depends, Query, status
from src.history.schemas import HistoryListResponse
from src.history.service import HistoryService
from src.history.dependencies import get_history_service

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
    description="Retrieves a list of previous distance calculations",
)
async def get_history(
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of records to return"
    ),
    service: HistoryService = Depends(get_history_service),
) -> HistoryListResponse:
    return await service.get_history(limit)
