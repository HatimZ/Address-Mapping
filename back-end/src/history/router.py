from fastapi import APIRouter, Depends, Query, status, Request
from fastapi.responses import JSONResponse
from src.history.schemas import HistoryListResponse
from src.history.service import HistoryService
from src.history.dependencies import get_history_service
from src.core.security import SecurityService, limiter
from src.core.exceptions import ValidationException, GeocodingException
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

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
@cache(
    expire=3600,
    namespace="history",
    key_builder=lambda *args, **kwargs: f"history:page:{kwargs['request'].query_params.get('page', '1')}:size:{kwargs['request'].query_params.get('page_size', '10')}",
)
async def get_history(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of records per page"),
    service: HistoryService = Depends(get_history_service),
) -> HistoryListResponse:
    response = await service.get_history(page=page, page_size=page_size)
    return JSONResponse(
        content=response.dict(),
        headers={
            "Access-Control-Allow-Origin": "http://localhost:5173",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Accept",
            "Access-Control-Allow-Credentials": "true",
        },
    )
