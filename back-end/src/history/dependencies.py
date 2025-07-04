from src.history.service import HistoryService
from src.core.clients.database.mongodb import MongoDBClient


async def get_history_service() -> HistoryService:
    database_client = MongoDBClient()
    return HistoryService(database_client)
