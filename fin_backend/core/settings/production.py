# settings/production.py
import os

from .base import *

DEBUG = False

# Security: In Production, the signing key MUST be a strong secret from ENV
SIMPLE_JWT["SIGNING_KEY"] = os.environ.get("JWT_SIGNING_KEY")

# Security: Enforce HTTPS-only for JWT-related cookies if you decide to use them
# and standard security headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Standard DRF Production settings
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ("rest_framework.renderers.JSONRenderer",)
