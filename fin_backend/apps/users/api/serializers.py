# users/serializers.py
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers


class RegistrationInputSerializer(serializers.Serializer):
    """Validates incoming payload for user registration."""

    email = serializers.EmailField()
    phone_number = PhoneNumberField(required=True)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs):
        # 1. Check if passwords match
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        # 2. Run Django's strict password validators (checks length, complexity, etc.)
        validate_password(attrs["password"])
        return attrs


class LoginInputSerializer(serializers.Serializer):
    """Validates incoming payload for user login."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
