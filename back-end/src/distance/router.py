from fastapi import APIRouter, Depends, HTTPException, status, Request
from src.distance.schemas import AddressRequest, DistanceResponse
from src.distance.service import DistanceService
from src.distance.dependencies import get_distance_service
from src.core.security import SecurityService, limiter
from src.core.exceptions import ValidationException, GeocodingException

from fastapi_cache.decorator import cache
from src.core.utils import invalidate_cache

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
@cache(
    expire=3600,
    namespace="distance",
    key_builder=lambda *args, **kwargs: f"distance:{kwargs['address_request'].address1}:{kwargs['address_request'].address2}",
)
async def calculate_distance(
    request: Request,
    address_request: AddressRequest,
    service: DistanceService = Depends(get_distance_service),
) -> DistanceResponse:
    try:
        result = await service.calculate_distance(
            address_request.address1, address_request.address2
        )
        await invalidate_cache("history", "history")
        return result
    except ValidationException as e:
        raise ValidationException(str(e))
    except Exception as e:
        raise GeocodingException("Failed to calculate distance", str(e))
