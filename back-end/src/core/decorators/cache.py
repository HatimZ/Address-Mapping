import functools
import hashlib
import json
from typing import Optional, Any, Callable
from fastapi import Request
from src.core.dependencies import get_cache_client
from src.core.clients.cache.cache import TTLCacheClient


def cache_response(
    namespace: str, ttl: int = 3600, key_generator: Optional[Callable] = None
):
    """
    Decorator to cache API responses.

    Args:
        namespace: Cache namespace for organizing cached data
        ttl: Time to live in seconds (default: 1 hour)
        key_generator: Custom function to generate cache keys
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Get cache client
            cache: TTLCacheClient = get_cache_client()

            # Generate cache key
            if key_generator:
                cache_key = key_generator(*args, **kwargs)
            else:
                cache_key = _generate_default_key(*args, **kwargs)

            # Try to get from cache first
            cached_result = await cache.get(cache_key, namespace)
            if cached_result:
                return cached_result

            # Execute the original function
            result = await func(*args, **kwargs)

            # Cache the result
            await cache.set(cache_key, result, namespace, ttl=ttl)

            return result

        return wrapper

    return decorator


def _generate_default_key(*args, **kwargs) -> str:
    """Generate a default cache key based on function arguments."""
    # Extract request and other relevant data
    request_data = {}

    for arg in args:
        if hasattr(arg, "dict"):  # Pydantic models
            request_data[str(type(arg))] = arg.dict()
        elif isinstance(arg, dict):
            request_data["dict_arg"] = arg
        else:
            request_data[str(type(arg))] = str(arg)

    for key, value in kwargs.items():
        if hasattr(value, "dict"):  # Pydantic models
            request_data[key] = value.dict()
        else:
            request_data[key] = value

    # Create a hash of the request data
    key_string = json.dumps(request_data, sort_keys=True, default=str)
    return hashlib.md5(key_string.encode()).hexdigest()


def cache_distance_calculation(func: Callable) -> Callable:
    """Specific decorator for distance calculation caching."""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Get cache client
        cache: TTLCacheClient = get_cache_client()

        # Extract address data for cache key
        address_request = None
        for arg in args:
            if hasattr(arg, "address1") and hasattr(arg, "address2"):
                address_request = arg
                break

        if not address_request:
            for value in kwargs.values():
                if hasattr(value, "address1") and hasattr(value, "address2"):
                    address_request = value
                    break

        if address_request:
            cache_key = f"{address_request.address1}:{address_request.address2}"

            # Try to get from cache first
            cached_result = await cache.get(cache_key, "distance")
            if cached_result:
                return cached_result

            # Execute the original function
            result = await func(*args, **kwargs)

            # Cache the result
            await cache.set(cache_key, result, "distance")

            # Clear history cache to ensure fresh data
            await cache.clear_namespace("history")

            return result
        else:
            # Fallback to original function if no address request found
            return await func(*args, **kwargs)

    return wrapper


def cache_history_query(func: Callable) -> Callable:
    """Specific decorator for history query caching."""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Get cache client
        cache: TTLCacheClient = get_cache_client()

        # Extract pagination parameters
        page = kwargs.get("page", 1)
        page_size = kwargs.get("page_size", 10)

        cache_key = f"page:{page}:size:{page_size}"

        # Try to get from cache first
        cached_result = await cache.get(cache_key, "history")
        if cached_result:
            return cached_result

        # Execute the original function
        result = await func(*args, **kwargs)

        # Cache the result
        await cache.set(cache_key, result, "history", ttl=3600)

        return result

    return wrapper
