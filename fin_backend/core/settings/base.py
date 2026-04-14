"""
Django base settings for Fintech Project.
Assumes file location: project_root/config/settings/base.py
"""

from datetime import timedelta
from pathlib import Path

import environ

# ------------------------------------------------------------------------------
# 1. PATHS & ENVIRONMENT CONFIGURATION
# ------------------------------------------------------------------------------
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR should point to the root of your repository.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize environ
env = environ.Env()
# We don't read .env here automatically in production, but it's safe fallback
# if the file exists in the base directory for local/docker setups.
environ.Env.read_env(BASE_DIR / ".env")


# ------------------------------------------------------------------------------
# 2. CORE DJANGO SETTINGS
# ------------------------------------------------------------------------------
# Security: Pull secret key from env. Crash immediately if not found.
SECRET_KEY = env("DJANGO_SECRET_KEY")

# Debug is FALSE by default. local.py will override this to True.
DEBUG = env.bool("DJANGO_DEBUG", False)

# Handled dynamically in local/prod
ALLOWED_HOSTS = []


# ------------------------------------------------------------------------------
# 3. APPLICATIONS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",  # Essential for Flutter Web / Mobile API requests
    "phonenumber_field",
    "drf_spectacular",
]

LOCAL_APPS = [
    "apps.users.apps.UsersConfig",  # Use the full path here!
    # 'wallets.apps.WalletsConfig', # (We will build this next)
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# ------------------------------------------------------------------------------
# 4. MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # MUST be at the very top
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "core.urls"

# ------------------------------------------------------------------------------
# 5. TEMPLATES & WSGI
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"


# ------------------------------------------------------------------------------
# 6. DATABASE & ACID TRANSACTIONS (FINTECH CRITICAL)
# ------------------------------------------------------------------------------
# We use env.db() to parse the DATABASE_URL (e.g. postgres://user:pass@host/db)
DATABASES = {"default": env.db("DATABASE_URL")}

# FINTECH MASTER RULE: ATOMIC REQUESTS
# Wraps every single HTTP request in a database transaction.
# If your view/service throws an exception, the entire database state
# for that request rolls back instantly. $O(1)$ effort for total data safety.
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)


# ------------------------------------------------------------------------------
# 7. AUTHENTICATION & USERS
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = "users.User"

# Strict password validation to prevent users from using "password123"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ------------------------------------------------------------------------------
# 8. DRF & JWT CONFIGURATION
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    # Pagination is critical for Ledger/Transactions to prevent memory crashes
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 50,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}


# ------------------------------------------------------------------------------
# 9. INTERNATIONALIZATION & TIMEZONES (AUDITABILITY)
# ------------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"

# FINTECH NON-NEGOTIABLE: Server time MUST be UTC.
# Never store local time in the database. Let Flutter handle the
# timezone conversion for the user's specific locale on the frontend.
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ------------------------------------------------------------------------------
# 10. STATIC & MEDIA FILES
# ------------------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SPECTACULAR_SETTINGS = {
    "TITLE": "Fintech Core API",
    "DESCRIPTION": "Enterprise API for Fintech App",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,  # Good for strict input/output separation
}
