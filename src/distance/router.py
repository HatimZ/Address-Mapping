from fastapi import APIRouter, Depends, HTTPException, status, Request
from src.distance.schemas import AddressRequest, DistanceResponse
from src.distance.service import DistanceService
from src.distance.dependencies import get_distance_service
from src.core.security import SecurityMiddleware, limiter
from src.core.exceptions import ValidationException, GeocodingException

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
) -> DistanceResponse:
    try:
        # Validate addresses
        address1 = await SecurityMiddleware.validate_address(address_request.address1)
        address2 = await SecurityMiddleware.validate_address(address_request.address2)

        # Validate IP
        await SecurityMiddleware.validate_ip(request)

        # Calculate distance
        return await service.calculate_distance(address1, address2)
    except ValidationException as e:
        raise ValidationException(str(e))
    except Exception as e:
        raise GeocodingException("Failed to calculate distance", str(e))
