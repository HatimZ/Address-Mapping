from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import get_settings

settings = get_settings()


def get_database():
    client = AsyncIOMotorClient(
        settings.mongodb_url,
        username=settings.mongodb_username,
        password=settings.mongodb_password,
    )
    return client[settings.mongodb_database]


db = get_database()
