from pydantic import BaseModel, Field, field_validator
from src.core.security import SecurityService
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class AddressRequest(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    address1: str = Field(
        ...,
        max_length=200,
        min_length=1,
        description="First address for distance calculation",
    )
    address2: str = Field(
        ...,
        max_length=200,
        min_length=1,
        description="Second address for distance calculation",
    )
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "address1": "New York Ny USA",
                "address2": "Toronto, Canada",
            }
        },
    )

    @field_validator("address1")
    def validate_address1(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Address must not be empty or whitespace")
        return SecurityService.validate_input(v)

    @field_validator("address2")
    def validate_address2(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Address must not be empty or whitespace")
        return SecurityService.validate_input(v)


class GeoLocation(BaseModel):
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    address: str = Field(..., description="Formatted address")


class DistanceModel(BaseModel):
    kilometers: float = Field(..., description="Distance in kilometers")
    miles: float = Field(..., description="Distance in miles")
    address1: GeoLocation = Field(..., description="Geocoded first address")
    address2: GeoLocation = Field(..., description="Geocoded second address")
    query_id: str = Field(..., description="Unique identifier for the query")
    coordinates: dict = Field(..., description="Coordinates for the addresses")
