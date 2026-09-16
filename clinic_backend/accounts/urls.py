from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CSRFGeneratorView, LogoutView, CookieTokenRefreshView

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    # CSRF cookie generator – call once on app load so React can read the token
    path("csrf/", CSRFGeneratorView.as_view(), name="csrf_cookie"),
    # Logout – blacklists refresh token and clears HttpOnly cookie
    path("logout/", LogoutView.as_view(), name="logout"),
    # Cookie-based token refresh – reads refresh from HttpOnly cookie
    path("users/token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
]
