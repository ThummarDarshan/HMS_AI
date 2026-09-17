# accounts/cookie_utils.py
"""
Utility functions for managing HttpOnly auth cookies.

Refresh tokens are stored in an HttpOnly cookie so they cannot be
accessed by JavaScript, reducing XSS risk. The access token is
returned in the JSON response body and stored in memory by the client.
"""

from django.conf import settings
from datetime import timedelta

# Cookie name for the refresh token
REFRESH_COOKIE_NAME = "refresh_token"

def get_cookie_max_age():
    return int(
        getattr(settings, "SIMPLE_JWT", {})
        .get("REFRESH_TOKEN_LIFETIME", timedelta(days=7))
        .total_seconds()
    )

def set_auth_cookie(response, refresh_token):
    """
    Attach the refresh token as an HttpOnly cookie to response.
    """
    max_age = get_cookie_max_age()
    is_secure = not settings.DEBUG or getattr(settings, 'SESSION_COOKIE_SECURE', False)
    samesite = getattr(settings, 'SESSION_COOKIE_SAMESITE', 'Lax')
    
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=str(refresh_token),
        max_age=max_age,
        secure=is_secure,
        httponly=True,
        samesite=samesite,
        path="/"
    )
    return response

def delete_auth_cookie(response):
    """
    Remove the refresh token cookie from response.
    """
    samesite = getattr(settings, 'SESSION_COOKIE_SAMESITE', 'Lax')
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path="/",
        samesite=samesite
    )
    return response

# Alias clear_auth_cookie to delete_auth_cookie
clear_auth_cookie = delete_auth_cookie

def get_refresh_from_cookie(request) -> str | None:
    """
    Read the refresh token from the HttpOnly cookie on request.
    Returns None if the cookie is absent.
    """
    return request.COOKIES.get(REFRESH_COOKIE_NAME)

