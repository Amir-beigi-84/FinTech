# users/services.py
from typing import Any, Dict

from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError, transaction
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@transaction.atomic
def register_user(validated_data: Dict[str, Any]) -> User:
    """
    Creates a new user safely.
    Returns the User instance.
    """
    # Remove password_confirm as it's not a model field
    validated_data.pop("password_confirm", None)
    password = validated_data.pop("password")

    try:
        # We use the CustomUserManager's create_user method which hashes the password!
        user = User.objects.create_user(password=password, **validated_data)
        return user
    except IntegrityError as e:
        # Catch DB constraint errors (e.g., email or phone already exists)
        # Fintech Rule: Don't expose raw DB errors.
        if "email" in str(e).lower():
            raise ValidationError({"email": "User with this email already exists."})
        if "phone_number" in str(e).lower():
            raise ValidationError({"phone_number": "User with this phone number already exists."})
        raise ValidationError("A database integrity error occurred.")


def login_user(email: str, password: str) -> Dict[str, str]:
    """
    Authenticates a user and returns JWT access and refresh tokens.
    """
    user = authenticate(email=email, password=password)

    if user is None:
        raise AuthenticationFailed("Invalid email or password.")

    if not user.is_active:
        raise AuthenticationFailed("This account has been deactivated.")

    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user_id": str(user.id),
        "email": user.email,
        "is_kyc_verified": user.is_kyc_verified,
    }
