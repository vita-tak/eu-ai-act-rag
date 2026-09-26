"""
CORS and rate limiting for the public API.

Registered from src/api/app.py: register_security() attaches CORS, and
rate_limit is applied to the API router as a dependency.

Rate limiting is applied as a dependency rather than through SlowAPIMiddleware
because slowapi finds routes by scanning app.routes for a matching endpoint,
and FastAPI 0.141 mounts included routers as a single opaque node instead of
flattening their routes. The middleware therefore finds no handler and lets
every request through silently. A dependency sees every request on the router,
so new endpoints are covered without touching them.
"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Browser origins allowed to call the API directly.
ALLOWED_ORIGINS = [
    "https://assistant.sarek.technology",
    "http://localhost:3000",
]

RATE_LIMITS = "20/minute;200/hour"

limiter = Limiter(key_func=get_remote_address, headers_enabled=True)


@limiter.shared_limit(RATE_LIMITS, scope="api")
async def rate_limit(request: Request, response: Response) -> None:
    """
    CORS and rate limiting for the public API.

    Registered from src/api/app.py via register_security() and the rate_limit dependency.
    """
    return None


def register_security(app: FastAPI) -> None:
    """Attach CORS and the rate limit error handler."""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type"],
    )
