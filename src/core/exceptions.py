from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Union
import traceback
from src.core.security import security_logger


class BaseAPIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        internal_error: Union[str, Exception] = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.internal_error = internal_error


class ValidationException(BaseAPIException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=f"Validation error: {detail}")


class GeocodingException(BaseAPIException):
    def __init__(self, detail: str, internal_error: Union[str, Exception] = None):
        super().__init__(
            status_code=422,
            detail=f"Geocoding error: {detail}",
            internal_error=internal_error,
        )


class DatabaseException(BaseAPIException):
    def __init__(self, detail: str, internal_error: Union[str, Exception] = None):
        super().__init__(
            status_code=500,
            detail="Database operation failed",
            internal_error=internal_error,
        )


async def exception_handler(request: Request, exc: BaseAPIException):
    # Log the error internally
    if exc.internal_error:
        security_logger.log_security_event(
            "Error", f"Path: {request.url.path}, Error: {str(exc.internal_error)}"
        )

    # Return a sanitized response
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "path": request.url.path},
    )


async def general_exception_handler(request: Request, exc: Exception):
    # Log the full error internally
    security_logger.log_security_event(
        "Unexpected Error",
        f"Path: {request.url.path}, Error: {str(exc)}\n{traceback.format_exc()}",
    )

    # Return a generic error response
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred", "path": request.url.path},
    )
