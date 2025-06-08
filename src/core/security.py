from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import List, Optional
import re
from datetime import datetime
import logging

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

# IP blacklist (in production, this should be in a database)
BLACKLISTED_IPS: List[str] = []
WHITELISTED_IPS: List[str] = []

# Address validation patterns
ADDRESS_PATTERN = re.compile(r"^[a-zA-Z0-9\s,.-]+$")
MAX_ADDRESS_LENGTH = 200


class SecurityMiddleware:
    @staticmethod
    async def validate_address(address: str) -> str:
        if not address or len(address) > MAX_ADDRESS_LENGTH:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid address format or length",
            )

        if not ADDRESS_PATTERN.match(address):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Address contains invalid characters",
            )

        return address.strip()

    @staticmethod
    async def validate_ip(request: Request) -> str:
        client_ip = request.client.host

        if client_ip in BLACKLISTED_IPS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )

        return client_ip

    @staticmethod
    async def validate_rate_limit(request: Request):
        if not WHITELISTED_IPS or request.client.host not in WHITELISTED_IPS:
            await limiter.check(request)


class SecurityLogger:
    def __init__(self):
        self.logger = logging.getLogger("security")
        self.logger.setLevel(logging.INFO)

        # File handler
        fh = logging.FileHandler("security.log")
        fh.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def log_request(self, request: Request, status: str, error: Optional[str] = None):
        self.logger.info(
            f"Request: {request.method} {request.url.path} - "
            f"IP: {request.client.host} - "
            f"Status: {status} - "
            f"Error: {error if error else 'None'}"
        )

    def log_security_event(self, event_type: str, details: str):
        self.logger.warning(f"Security Event: {event_type} - {details}")


security_logger = SecurityLogger()
