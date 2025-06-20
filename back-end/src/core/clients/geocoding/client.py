import httpx
from typing import Dict, Any
from src.config import get_settings
from src.core.clients.geocoding.base import GeocodingClient
from src.core.clients.geocoding.exceptions import GeocodingError
from src.config import logger
from src.distance.schemas import GeoLocation
from asyncio_throttle import Throttler

settings = get_settings()


class NominatimClient(GeocodingClient):
    def __init__(self):
        super().__init__()
        self.base_url = settings.NOMINATIM_BASE_URL
        self.headers = {"User-Agent": settings.NOMINATIM_USER_AGENT}
        self.timeout = settings.NOMINATIM_TIMEOUT
        self.throttler = Throttler(rate_limit=1, period=1)

    async def geocode(self, address: str) -> GeoLocation:
        """Actual geocoding implementation with throttling."""
        async with self.throttler:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                try:
                    response = await client.get(
                        f"{self.base_url}/search",
                        params={"q": address, "format": "json", "limit": 1},
                        headers=self.headers,
                    )

                    logger.info(f"Response Status: {response.status_code}")
                    logger.info(f"Response Headers: {dict(response.headers)}")
                    logger.info(f"Response URL: {response.url}")
                    logger.info(f"Response Content: {response.text}")

                    response.raise_for_status()
                    results = response.json()

                    if not results:
                        print("NO RESULTSS")
                        raise GeocodingError(
                            f"No results found for address: {address}. The GeoCoding Client cannot code this address."
                        )

                    result: dict = results[0]

                    return GeoLocation(
                        latitude=float(result.get("lat")),
                        longitude=float(result.get("lon")),
                        address=result.get("display_name"),
                    )
                except httpx.HTTPError as e:
                    raise GeocodingError(f"Geocoding service error: {str(e)}")
                except (KeyError, ValueError) as e:
                    raise GeocodingError(f"Invalid response format: {str(e)}")
