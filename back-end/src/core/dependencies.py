from src.core.clients.cache.cache import TTLCacheClient

# Create a singleton instance
_cache_client = TTLCacheClient(maxsize=1000, ttl=3600)


def get_cache_client() -> TTLCacheClient:
    """Get the cache client instance."""
    return _cache_client
