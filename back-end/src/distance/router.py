from fastapi import APIRouter, Depends, status, Request
from src.distance.schemas import AddressRequest, DistanceResponse
from src.distance.service import DistanceService
from src.distance.dependencies import get_distance_service
from src.core.security import limiter
from src.core.exceptions import ValidationException, GeocodingException
from src.core.dependencies import get_cache_client
from src.core.clients.cache.cache import TTLCacheClient
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/distance",
    tags=["Distance Calculation"],
    responses={
        400: {"description": "Invalid input"},
        500: {"description": "Internal server error"},
    },
)


@router.post(
    "/calculate",
    response_model=DistanceResponse,
    status_code=status.HTTP_200_OK,
    summary="Calculate distance between two addresses",
    description="Geocodes two addresses and calculates the distance between them in kilometers",
)
@limiter.limit("5/minute")
async def calculate_distance(
    request: Request,
    address_request: AddressRequest,
    service: DistanceService = Depends(get_distance_service),
    cache: TTLCacheClient = Depends(get_cache_client),
) -> DistanceResponse:
    try:
        # Try to get from cache first
        cache_key = f"{address_request.address1}:{address_request.address2}"
        cached_result = await cache.get(cache_key, "distance")
        if cached_result:
            return cached_result

        result = await service.calculate_distance(
            address_request.address1, address_request.address2
        )

        await cache.set(cache_key, result, "distance", ttl=3600)
        await cache.clear_namespace("history")

        return result
    except ValidationException as e:
        raise ValidationException(str(e))
    except Exception as e:
        error = str(e)
        status = 500
        if service.errors:
            error = service.errors
            status = 400
        return JSONResponse(status_code=status, content={"errors": error})
