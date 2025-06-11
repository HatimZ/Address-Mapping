from typing import Any, Dict, Optional
from cachetools import TTLCache
from .base import BaseCacheClient
import logging

logger = logging.getLogger(__name__)


class TTLCacheClient(BaseCacheClient):
    """TTLCache implementation of the cache client."""

    def __init__(self, maxsize: int = 1000, ttl: int = 3600):
        """
        Initialize the cache client.

        Args:
            maxsize: Maximum number of items in cache
            ttl: Default time-to-live in seconds
        """
        self._cache: Dict[str, TTLCache] = {}
        self._maxsize = maxsize
        self._default_ttl = ttl

    def _get_namespace_cache(self, namespace: str) -> TTLCache:
        """Get or create a TTLCache for a namespace."""
        if namespace not in self._cache:
            self._cache[namespace] = TTLCache(
                maxsize=self._maxsize, ttl=self._default_ttl
            )
        return self._cache[namespace]

    def _get_key(self, key: str, namespace: str) -> str:
        """Get the full cache key including namespace."""
        return f"{namespace}:{key}"

    async def get(self, key: str, namespace: str) -> Optional[Any]:
        """Get a value from cache."""
        try:
            cache = self._get_namespace_cache(namespace)
            full_key = self._get_key(key, namespace)
            return cache.get(full_key)
        except Exception as e:
            logger.error(f"Error getting from cache: {str(e)}")
            return None

    async def set(
        self, key: str, value: Any, namespace: str, ttl: Optional[int] = None
    ) -> None:
        """Set a value in cache with optional TTL."""
        try:
            cache = self._get_namespace_cache(namespace)
            full_key = self._get_key(key, namespace)
            if ttl:
                # Create a new TTLCache with custom TTL for this key
                temp_cache = TTLCache(maxsize=1, ttl=ttl)
                temp_cache[full_key] = value
                cache.update(temp_cache)
            else:
                cache[full_key] = value
        except Exception as e:
            logger.error(f"Error setting cache: {str(e)}")

    async def delete(self, key: str, namespace: str) -> None:
        """Delete a specific key from cache."""
        try:
            cache = self._get_namespace_cache(namespace)
            full_key = self._get_key(key, namespace)
            cache.pop(full_key, None)
        except Exception as e:
            logger.error(f"Error deleting from cache: {str(e)}")

    async def clear_namespace(self, namespace: str) -> None:
        """Clear all keys in a namespace."""
        try:
            if namespace in self._cache:
                self._cache[namespace].clear()
        except Exception as e:
            logger.error(f"Error clearing namespace: {str(e)}")

    async def clear_all(self) -> None:
        """Clear all cache entries."""
        try:
            for namespace in self._cache:
                self._cache[namespace].clear()
        except Exception as e:
            logger.error(f"Error clearing all cache: {str(e)}")
