# settings/local.py
from .base import *

DEBUG = True

# Add the Browsable API so you can test endpoints in the browser easily
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += ("rest_framework.renderers.BrowsableAPIRenderer",)

# Use a simple signing key for local development
SIMPLE_JWT["SIGNING_KEY"] = "dev-secret-key-123"
