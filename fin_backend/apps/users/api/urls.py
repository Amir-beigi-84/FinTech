from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

# Make sure you import both your Login AND Registration views here!
from apps.users.api.views import LoginAPIView, RegistrationAPIView

urlpatterns = [
    # Registration / Sign Up
    path("auth/register/", RegistrationAPIView.as_view(), name="register"),
    # Login / Sign In
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    # JWT Refresh
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
