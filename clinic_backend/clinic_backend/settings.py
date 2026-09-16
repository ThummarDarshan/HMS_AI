from pathlib import Path
from datetime import timedelta
import os
from decouple import config
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Core secrets – must be set in environment
# ---------------------------------------------------------------------------
SECRET_KEY = config("SECRET_KEY", default="django-insecure-change-this-in-production")

JWT_SIGNING_KEY = config("JWT_SIGNING_KEY", default=None)
if not JWT_SIGNING_KEY:
    raise ImproperlyConfigured(
        "JWT_SIGNING_KEY environment variable is required. "
        "Set it to a strong random string that is DIFFERENT from SECRET_KEY."
    )
if JWT_SIGNING_KEY == SECRET_KEY:
    raise ImproperlyConfigured(
        "JWT_SIGNING_KEY must be different from SECRET_KEY. "
        "Using the same key for both is a security risk."
    )

ENCRYPTION_KEY = config("ENCRYPTION_KEY", default=None)
if not ENCRYPTION_KEY:
    raise ImproperlyConfigured(
        "ENCRYPTION_KEY environment variable is required. "
        "Generate one with: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
    )

# Validate ENCRYPTION_KEY is a valid Fernet key
try:
    from cryptography.fernet import Fernet, InvalidToken
    Fernet(ENCRYPTION_KEY.encode())
except Exception:
    raise ImproperlyConfigured(
        "ENCRYPTION_KEY is not a valid Fernet key. "
        "Generate one with: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
    )

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1,0.0.0.0").split(",")

# ---------------------------------------------------------------------------
# Application definition
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "cloudinary",
    "cloudinary_storage",
    # Custom apps
    "accounts",
    "patients",
    "doctors",
    "appointments",
    "records",
    "billing",
    "support",
    "beds",
    "laboratory",
    "ai_assistant",
]

# Cloudinary Configuration
import cloudinary

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME", default=""),
    "API_KEY": config("CLOUDINARY_API_KEY", default=""),
    "API_SECRET": config("CLOUDINARY_API_SECRET", default=""),
}

# Initialize cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE["CLOUD_NAME"],
    api_key=CLOUDINARY_STORAGE["API_KEY"],
    api_secret=CLOUDINARY_STORAGE["API_SECRET"],
    secure=True,
)

# Use Cloudinary for media file storage
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "clinic_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "clinic_backend.wsgi.application"

# ---------------------------------------------------------------------------
# Database – PostgreSQL only (SQLite is not supported in production)
# ---------------------------------------------------------------------------
_db_url = config(
    "DATABASE_URL",
    default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}" if DEBUG else None,
)
if not _db_url:
    raise ImproperlyConfigured(
        "DATABASE_URL environment variable is required in production. "
        "Set it to a valid PostgreSQL connection string."
    )

DATABASES = {
    "default": dj_database_url.parse(
        _db_url,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Enforce PostgreSQL in production
if not DEBUG and "postgresql" not in DATABASES["default"]["ENGINE"]:
    raise ImproperlyConfigured(
        "Only PostgreSQL is supported. "
        f"Got engine: {DATABASES['default']['ENGINE']}"
    )

# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 10},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# ---------------------------------------------------------------------------
# Default primary key field type
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Custom User Model
# ---------------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# ---------------------------------------------------------------------------
# REST Framework Configuration – with Rate Limiting
# ---------------------------------------------------------------------------
THROTTLE_ANON_RATE = config("THROTTLE_ANON_RATE", default="60/min")
THROTTLE_USER_RATE = config("THROTTLE_USER_RATE", default="1000/min")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    # Rate limiting
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": THROTTLE_ANON_RATE,
        "user": THROTTLE_USER_RATE,
    },
}

# ---------------------------------------------------------------------------
# JWT Settings – separate signing key, short-lived access tokens, rotation
# ---------------------------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": JWT_SIGNING_KEY,   # ← uses its own key, NOT SECRET_KEY
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# ---------------------------------------------------------------------------
# CORS Settings
# ---------------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:8080,http://127.0.0.1:8080,http://localhost:3000,http://127.0.0.1:3000",
).split(",")

# ---------------------------------------------------------------------------
# CSRF Settings
# ---------------------------------------------------------------------------
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="http://localhost:8080,http://127.0.0.1:8080,http://localhost:3000,http://127.0.0.1:3000",
).split(",")
# Must be False so the React frontend JS can read the cookie value
CSRF_COOKIE_HTTPONLY = False

# ---------------------------------------------------------------------------
# Security Headers (enforced in production only)
# ---------------------------------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SECURE_HSTS_SECONDS = 31536000          # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

# ---------------------------------------------------------------------------
# Email Configuration
# ---------------------------------------------------------------------------
EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL", default="noreply@clinicmanagement.com"
)

# ---------------------------------------------------------------------------
# Password Reset Token Expiration (in hours)
# ---------------------------------------------------------------------------
PASSWORD_RESET_TOKEN_EXPIRATION_HOURS = config(
    "PASSWORD_RESET_TOKEN_EXPIRATION_HOURS", default=24, cast=int
)

# Frontend URL for password reset link
FRONTEND_URL = config("FRONTEND_URL", default="http://localhost:3000")
