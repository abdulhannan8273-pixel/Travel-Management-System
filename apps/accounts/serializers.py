from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "phone", "profile_image", "created_at",]
        read_only_fields = ["id", "username", "created_at"]

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("old password is incorrect")
        return value
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address")
        return value
    
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=6)

class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address")
        return value