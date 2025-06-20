from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from src.distance.schemas import GeoLocation


class GeocodingClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def geocode(self, address: str) -> GeoLocation:
        """Geocode an address with rate limiting enforced by the implementation."""
        return await self._geocode_implementation(address)
