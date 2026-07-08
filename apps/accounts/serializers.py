from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password"]
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone=validated_data.get("phone", ""),
            password=validated_data["password"]
        )

        verify_link = f"http://127.0.0.1:8000/api/accounts/verify-email/{user.email_verification_token}/"
        send_mail(
            subject="Verify your email",
            message=f"Please click the link to verify your email: {verify_link}",
            from_email="noreply@yourdomain.com",
            recipient_list=[user.email],
        )
        return user
    

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            email=attrs["email"],
            password=attrs["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        if not getattr(user, "is_email_verified", True):
            raise serializers.ValidationError(
                "Please verify your email before logging in."
            )

        attrs["user"] = user
        return attrs


import re
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "profile_image",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "username",
            "email",
            "created_at",
        ]
    def validate_profile_image(self, value):
        if not value:
            return value

        # Maximum file size: 2 MB
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError(
                "Image size must not exceed 2 MB."
            )

        # Allowed extensions
        allowed_extensions = ["jpg", "jpeg", "png", "webp"]

        extension = value.name.split(".")[-1].lower()

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Only JPG, JPEG, PNG and WEBP images are allowed."
            )

        return value

    def validate_phone(self, value):
        if value and not re.fullmatch(r"^[6-9]\d{9}$", value):
            raise serializers.ValidationError(
                "Enter a valid 10-digit Indian mobile number."
            )
        return value
       
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("old password is incorrect")
        return value
    
    def validate_new_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address")
        return value
    
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address")
        return value