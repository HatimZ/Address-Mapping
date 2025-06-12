from abc import ABC, abstractmethod
from typing import Dict, Any
from src.distance.schemas import GeoLocation


class GeocodingClient(ABC):
    @abstractmethod
    async def geocode(self, address: str) -> GeoLocation:
        pass
