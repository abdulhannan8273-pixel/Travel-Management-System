from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import RegisterSerializer,LoginSerializer,ProfileSerializer,ChangePasswordSerializer,ForgotPasswordSerializer, ResendVerificationSerializer, ResetPasswordSerializer, ResendVerificationSerializer
from .models import User


class RegisterView(CreateAPIView):
    queryset = User .objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "message": "User registered succesfully."}, status=status.HTTP_201_CREATED)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({"success": True, "message": "Login successful.", "access": str(refresh.access_token), "refresh": str(refresh)}, status=status.HTTP_200_OK)

class ProfileView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"success": True, "message": "Password changed successfully."}, status=status.HTTP_200_OK)
    
class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": True, "message": "Logout successful."}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"success": False, "message": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        reset_link = f"http://127.0.0.1:8000/api/accounts/reset-password/{uid}/{token}/"
        send_mail(
            subject="Reset your password",
            message=f"Click this link to reset your password: {reset_link}",
            from_email="noreply@travelapp.com",
            recipient_list=[email],
                )
        return Response({"success": True, "message": "Password reset link sent to your email."}, 
                        status=status.HTTP_200_OK)
    
class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, uid, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, TypeError, ValueError, OverflowError):
            return Response({"success": False, "message": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"success": False, "message": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"success": True, "message": "Password reset successful."}, status=status.HTTP_200_OK)
    
class VerifyEmailView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            user = User.objects.get(email_verification_token=token)
        except (User.DoesNotExist, ValueError):
            return Response({"success": False, "message": "Invalid verification token."}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
        user.is_email_verified = True
        user.save()
        return Response({"success": True, "message": "Email verified successfully."}, status=status.HTTP_200_OK)
    
class ResendVerificationView(GenericAPIView):
    serializer_class = ResendVerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        if user.is_email_verified:
            return Response({"success": False, "message": "Email is already verified."}, status=status.HTTP_400_BAD_REQUEST)
        verify_link = f"http://127.0.0.1:8000/api/accounts/verify-email/{user.email_verification_token}/"
        send_mail(
            subject="Verify your email",
            message=f"Please click the link to verify your email: {verify_link}",
            from_email="noreply@yourdomain.com",
            recipient_list=[email],
        )
        return Response({"success": True, "message": "Verification link sent to your email."}, status=status.HTTP_200_OK)