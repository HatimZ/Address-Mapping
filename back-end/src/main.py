from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse


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
    version=settings.VERSION,
    description="API for calculating distances between addresses and retrieving query history",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
    default_response_class=JSONResponse,
    default_response_headers={},  # Disable default headers
)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


origins = [
    "localhost:5173",
    "http://localhost:5174",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    settings.PUBLIC_API_URL,
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


app.include_router(distance_router, prefix=settings.API_PREFIX)
app.include_router(history_router, prefix=settings.API_PREFIX)


#
