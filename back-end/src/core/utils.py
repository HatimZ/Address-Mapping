import logging
from src.core.dependencies import get_cache_client

logger = logging.getLogger(__name__)


async def invalidate_cache(
    namespace: str,
    key: str = None,
) -> None:
    """Invalidate cache for specific addresses"""
    try:
        cache = get_cache_client()
        if key:
            await cache.delete(key, namespace)
        else:
            await cache.clear_namespace(namespace)

        logger.error(f"Invalidated cache: {namespace} {key}")
    except Exception as ex:
        logger.error(f"Error invalidateing cache: {namespace} {key} : {str(ex)}")
