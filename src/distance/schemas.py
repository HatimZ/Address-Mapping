from pydantic import BaseModel, Field
from typing import Optional


class AddressRequest(BaseModel):
    address1: str = Field(..., description="First address for distance calculation")
    address2: str = Field(..., description="Second address for distance calculation")


class GeoLocation(BaseModel):
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    address: str = Field(..., description="Formatted address")


class DistanceResponse(BaseModel):
    distance_km: float = Field(..., description="Distance in kilometers")
    address1: GeoLocation = Field(..., description="Geocoded first address")
    address2: GeoLocation = Field(..., description="Geocoded second address")
    query_id: str = Field(..., description="Unique identifier for the query")
