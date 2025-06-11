from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
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


class SearchQuery(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    address1: str = Field(..., description="First address for distance calculation")
    address2: str = Field(..., description="Second address for distance calculation")
    distance_km: float = Field(..., description="Calculated distance in kilometers")
    coordinates: dict = Field(
        ..., description="Geographic coordinates of both addresses"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    ip_address: str = Field(..., description="IP address of the requester")
    user_agent: Optional[str] = Field(None, description="User agent of the requester")
    status: str = Field(default="success", description="Status of the query")
    error_message: Optional[str] = Field(
        None, description="Error message if query failed"
    )

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}
        schema_extra = {
            "example": {
                "address1": "New York, NY",
                "address2": "Los Angeles, CA",
                "distance_km": 3935.5,
                "coordinates": {
                    "point1": [40.7128, -74.0060],
                    "point2": [34.0522, -118.2437],
                },
                "ip_address": "192.168.1.1",
                "user_agent": "Mozilla/5.0...",
                "status": "success",
            }
        }
