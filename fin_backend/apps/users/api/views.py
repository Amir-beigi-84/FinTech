# users/views.py
from drf_spectacular.utils import extend_schema  # <-- Import this!
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.services import login_user, register_user

from .serializers import LoginInputSerializer, RegistrationInputSerializer


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationInputSerializer  # <-- Add this hint for Swagger

    @extend_schema(
        summary="Register a new user",
        description="Creates a new user and returns JWT tokens.",
        request=RegistrationInputSerializer,
        responses={201: dict},
    )
    def post(self, request):
        # 1. Validate payload
        serializer = RegistrationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Execute Business Logic
        user = register_user(validated_data=serializer.validated_data)

        # 3. Automatically log the user in after signup
        tokens_data = login_user(
            email=serializer.validated_data["email"],
            password=request.data.get("password"),
        )

        return Response(
            {"message": "User registered successfully.", "data": tokens_data},
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginInputSerializer  # <-- Add this hint for Swagger

    @extend_schema(
        summary="Login user",
        description="Authenticates a user and returns JWT access and refresh tokens.",
        request=LoginInputSerializer,
        responses={200: dict},
    )
    def post(self, request):
        serializer = LoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens_data = login_user(
            email=serializer.validated_data.get("email"),
            password=serializer.validated_data.get("password"),
        )

        return Response(tokens_data, status=status.HTTP_200_OK)
