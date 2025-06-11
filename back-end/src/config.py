from pydantic_settings import BaseSettings
from functools import lru_cache
import logging
import sys


class Settings(BaseSettings):
    APP_NAME: str = "Address Distance API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    MONGODB_URL: str
    MONGODB_PASSWORD: str
    MONGODB_USERNAME: str
    NOMINATIM_BASE_URL: str = "https://nominatim.openstreetmap.org"
    NOMINATIM_USER_AGENT: str = "AddressDistanceAPI/1.0"
    NOMINATIM_TIMEOUT: int = 10
    HISTORY_LIMIT: int = 100

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


def setup_logger(name: str = None) -> logging.Logger:
    """
    Set up and return a simple console logger.

    Args:
        name (str, optional): Name of the logger. If None, returns the root logger.

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger("address_distance_api")
