from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class DatabaseClient(ABC):
    """Database-agnostic client interface that can work with any database."""

    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> str:
        """
        Create a new record in the database.

        Args:
            data: Dictionary containing the record data

        Returns:
            str: ID of the created record
        """
        pass

    @abstractmethod
    async def find_one(self, id: str):
        """
        Find one document with the specified id

        Args:
            id: Dictionary containing the record data

        Returns:
            str: ID of the created record
        """
        pass

    @abstractmethod
    async def find_many(
        self,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Find multiple records with pagination and sorting.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            sort_by: Field to sort by
            sort_order: Sort order ('asc' or 'desc')
            filters: Optional filters to apply

        Returns:
            List of records
        """
        pass

    @abstractmethod
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count total number of records.

        Args:
            filters: Optional filters to apply

        Returns:
            Total count of records
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the database connection."""
        pass
