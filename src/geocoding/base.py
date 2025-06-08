from abc import ABC, abstractmethod
from typing import Dict, Any


class GeocodingClient(ABC):
    @abstractmethod
    async def geocode(self, address: str) -> Dict[str, Any]:
        pass
