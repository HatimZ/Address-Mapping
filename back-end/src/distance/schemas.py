from pydantic import BaseModel, Field, field_validator
from src.core.security import SecurityService


class AddressRequest(BaseModel):
    address1: str = Field(
        ..., max_length=200, description="First address for distance calculation"
    )
    address2: str = Field(
        ..., max_length=200, description="Second address for distance calculation"
    )

    @field_validator("address1")
    def validate_address1(cls, v: str) -> str:
        return SecurityService.validate_input(v)

    @field_validator("address2")
    def validate_address2(cls, v: str) -> str:
        return SecurityService.validate_input(v)


class GeoLocation(BaseModel):
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    address: str = Field(..., description="Formatted address")


class DistanceResponse(BaseModel):
    kilometers: float = Field(..., description="Distance in kilometers")
    miles: float = Field(..., description="Distance in miles")
    address1: GeoLocation = Field(..., description="Geocoded first address")
    address2: GeoLocation = Field(..., description="Geocoded second address")
    query_id: str = Field(..., description="Unique identifier for the query")
