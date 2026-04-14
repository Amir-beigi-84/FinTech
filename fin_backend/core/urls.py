from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("apps.users.api.urls")),
    # OpenAPI 3 schema generation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # Convenience Redirects
    path("", RedirectView.as_view(url="/api/docs/", permanent=False)),
    path("api/v1/", RedirectView.as_view(url="/api/docs/", permanent=False)),
]
