from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # MongoDB settings
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_username: Optional[str] = None
    mongodb_password: Optional[str] = None
    mongodb_database: str = "address_distance"

    # Nominatim settings
    nominatim_base_url: str = "https://nominatim.openstreetmap.org"
    nominatim_user_agent: str = "AddressDistanceAPI/1.0"

    # API settings
    api_prefix: str = "/api/v1"
    debug: bool = False

    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 3600  # 1 hour in seconds

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
