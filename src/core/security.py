from fastapi import Request, HTTPException, status
from pydantic import ValidationError
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import List, Optional
import re
import html
from bleach import clean
import logging


logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)


BLACKLISTED_IPS: List[str] = []
WHITELISTED_IPS: List[str] = []


ADDRESS_PATTERN = re.compile(r"^[a-zA-Z0-9\s,.-]+$")
MAX_ADDRESS_LENGTH = 200


SQL_PATTERN = re.compile(
    r"(?i)(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|TRUNCATE|EXEC|DECLARE)"
)
HTML_PATTERN = re.compile(r"<[^>]*>")
SCRIPT_PATTERN = re.compile(r"<script.*?>.*?</script>", re.IGNORECASE | re.DOTALL)
COMMAND_PATTERN = re.compile(r"[;&|`$]")


class SecurityService:
    @staticmethod
    def validate_input(input: str) -> str:
        # Checking for SQL injection attempts
        if SQL_PATTERN.search(input):
            logger.warning(
                f"Potential SQL injection attempt detected in address1: {input}"
            )
            raise ValidationError("Invalid address format")

        # Checking for HTML/script injection
        if HTML_PATTERN.search(input) or SCRIPT_PATTERN.search(input):
            logger.warning(
                f"Potential HTML/script injection attempt detected in address1: {input}"
            )
            raise ValidationError("Invalid address format")

        # Checking for command injection
        if COMMAND_PATTERN.search(input):
            logger.warning(
                f"Potential command injection attempt detected in address1: {input}"
            )
            raise ValidationError("Invalid address format")

        # Sanitizing the input
        sanitized = clean(input, strip=True)
        sanitized = html.escape(sanitized)

        # Removinh any remaining potentially dangerous characters
        sanitized = re.sub(r"[^\w\s,.-]", "", sanitized)

        return sanitized.strip()

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
