from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseCacheClient(ABC):
    """Base class for cache clients defining the interface for cache operations."""

    @abstractmethod
    async def get(self, key: str, namespace: str) -> Optional[Any]:
        """Get a value from cache."""
        pass

    @abstractmethod
    async def set(
        self, key: str, value: Any, namespace: str, ttl: Optional[int] = None
    ) -> None:
        """Set a value in cache with optional TTL."""
        pass

    @abstractmethod
    async def delete(self, key: str, namespace: str) -> None:
        """Delete a specific key from cache."""
        pass

    @abstractmethod
    async def clear_namespace(self, namespace: str) -> None:
        """Clear all keys in a namespace."""
        pass

    @abstractmethod
    async def clear_all(self) -> None:
        """Clear all cache entries."""
        pass
