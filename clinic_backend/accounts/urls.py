from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CookieTokenRefreshView, LogoutView, CSRFGeneratorView

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("csrf/", CSRFGeneratorView.as_view(), name="csrf"),
    path("logout/", LogoutView.as_view(), name="logout_direct"),
    path("users/logout/", LogoutView.as_view(), name="logout"),
    path("users/token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
]

