from django.urls import path
from .views import RegisterView, LoginView, ProfileView, ChangePasswordView, LogoutView, ForgotPasswordView, ResetPasswordView, VerifyEmailView, ResendVerificationView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/<str:uid>/<str:token>/", ResetPasswordView.as_view(), name="reset-password"),
    path("verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("resend-verification/", ResendVerificationView.as_view(), name="resend-verification"),
]
