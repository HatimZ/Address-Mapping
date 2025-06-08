from abc import ABC, abstractmethod
from typing import List, Dict, Any


class DatabaseClient(ABC):
    @abstractmethod
    async def save_query(self, query_data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    async def get_history(self, limit: int) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_total_queries(self) -> int:
        pass
