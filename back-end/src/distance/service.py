from geopy.distance import geodesic
from src.distance.schemas import DistanceResponse, GeoLocation
from src.core.clients.geocoding.base import GeocodingClient
from src.core.clients.database.base import DatabaseClient
from src.distance.exceptions import DistanceCalculationError
from src.config import logger


class DistanceService:
    def __init__(
        self, geocoding_client: GeocodingClient, database_client: DatabaseClient
    ):
        self.geocoding_client = geocoding_client
        self.database_client = database_client
        self.errors = []

    async def calculate_distance(
        self, address1: str, address2: str
    ) -> DistanceResponse:

        try:
            location1 = await self.geocoding_client.geocode(address1)

        except Exception as ex:
            self.errors.append(str(ex))

        try:
            location2 = await self.geocoding_client.geocode(address2)

        except Exception as ex:
            self.errors.append(str(ex))

        print(self.errors)
        if self.errors:

            raise DistanceCalculationError(f"Failed to calculate distance")

        logger.info(location1)
        logger.info(location2)
        point1 = (location1.latitude, location1.longitude)
        point2 = (location2.latitude, location2.longitude)

        kilometers = geodesic(point1, point2).kilometers
        miles = geodesic(point1, point2).miles

        query_data = {
            "kilometers": kilometers,
            "miles": miles,
            "address1": location1.address,
            "address2": location2.address,
            "coordinates": {"point1": point1, "point2": point2},
        }

        query_id = await self.database_client.create(query_data)

        return DistanceResponse(
            kilometers=round(kilometers, 2),
            miles=round(miles, 2),
            address1=location1,
            address2=location2,
            query_id=query_id,
        )
