from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from src.config import get_settings
from src.distance.router import router as distance_router
from src.history.router import router as history_router
from src.core.security import limiter, SecurityMiddleware, security_logger
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
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API for calculating distances between addresses and retrieving query history",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(BaseAPIException, exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


# Add middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        response = await call_next(request)
        security_logger.log_request(request, "success")
        return response
    except Exception as e:
        security_logger.log_request(request, "error", str(e))
        raise


# Add routers
app.include_router(distance_router, prefix=settings.API_PREFIX)
app.include_router(history_router, prefix=settings.API_PREFIX)
