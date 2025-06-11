from fastapi_cache import FastAPICache


async def invalidate_cache(key: str, namespace: str):
    """Invalidate cache for specific addresses"""
    await FastAPICache.clear(namespace=namespace, key=key)
    return True
