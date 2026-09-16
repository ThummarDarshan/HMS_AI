# accounts/cookie_utils.py
"""
Utility functions for managing HttpOnly auth cookies.

Refresh tokens are stored in an HttpOnly cookie so they cannot be
accessed by JavaScript, reducing XSS risk.  The access token is
returned in the JSON response body and stored in memory by the client.
"""

from django.conf import settings

# Cookie name for the refresh token
REFRESH_COOKIE_NAME = "refresh_token"

# Cookie lifetime matches the JWT refresh token lifetime
COOKIE_MAX_AGE = int(
    getattr(settings, "SIMPLE_JWT", {})
    .get("REFRESH_TOKEN_LIFETIME", __import__("datetime").timedelta(days=7))
    .total_seconds()
)


def set_auth_cookie(response, refresh_token: str) -> None:
    """
    Attach the refresh token as an HttpOnly cookie to *response*.

    Flags:
      - httponly=True  → JS cannot read it (XSS protection)
      - samesite='Lax' → CSRF protection for cross-site requests
      - secure=True    → Only sent over HTTPS (in production)
    """
    is_secure = not settings.DEBUG

    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        samesite="Lax",
        secure=is_secure,
        path="/",
    )


def clear_auth_cookie(response) -> None:
    """
    Remove the refresh token cookie from *response* (used during logout).
    """
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path="/",
        samesite="Lax",
    )


def get_refresh_from_cookie(request) -> str | None:
    """
    Read the refresh token from the HttpOnly cookie on *request*.
    Returns None if the cookie is absent.
    """
    return request.COOKIES.get(REFRESH_COOKIE_NAME)
