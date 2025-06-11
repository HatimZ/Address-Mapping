from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from src.config import get_settings
from src.distance.router import router as distance_router
from src.history.router import router as history_router
from src.core.security import limiter, SecurityService, security_logger
from src.core.exceptions import (
    BaseAPIException,
    ValidationException,
    GeocodingException,
    DatabaseException,
    exception_handler,
    general_exception_handler,
)

settings = get_settings()

app = FastAPI(
    title="Address Distance API",
    description="API for calculating distances between addresses",
    version="1.0.0",
)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


origins = [
    "localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


app.add_exception_handler(BaseAPIException, exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.add_middleware(SlowAPIMiddleware)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        response = await call_next(request)
        security_logger.log_request(request, "success")
        return response
    except Exception as e:
        security_logger.log_request(request, "error", str(e))
        raise


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())


app.include_router(distance_router, prefix=settings.API_PREFIX)
app.include_router(history_router, prefix=settings.API_PREFIX)


#
