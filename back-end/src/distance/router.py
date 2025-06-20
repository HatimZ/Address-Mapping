from fastapi import APIRouter, Depends, status, Request, Body
from src.distance.schemas import AddressRequest, DistanceResponse
from src.distance.service import DistanceService
from src.distance.dependencies import get_distance_service
from src.core.security import limiter
from src.core.exceptions import ValidationException, GeocodingException
from src.core.decorators.cache import cache_distance_calculation
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
    description="Geocodes two addresses and calculates the distance between them in kilometers and miles",
)
@limiter.limit("1/second")
@cache_distance_calculation
async def calculate_distance(
    request: Request,
    address_request: AddressRequest = Body(...),
    service: DistanceService = Depends(get_distance_service),
) -> DistanceResponse:
    try:
        result = await service.calculate_distance(
            address_request.address1, address_request.address2
        )
        return result
    except ValidationException as e:
        raise ValidationException(str(e))
    except Exception as e:
        error = str(e)
        status_code = 500
        if service.errors:
            error = service.errors
            status_code = 400
        return JSONResponse(status_code=status_code, content={"errors": error})
