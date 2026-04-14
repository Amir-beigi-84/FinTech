import os

from django.core.wsgi import get_wsgi_application

# Point to your local settings by default
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

application = get_wsgi_application()
