from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, RazorpayWebhookView

router = DefaultRouter()

router.register(
    r"payments",
    PaymentViewSet,
    basename="payment",
)

urlpatterns = [
    path("payments/razorpay-webhook/", RazorpayWebhookView.as_view(), name="razorpay-webhook"),
] + router.urls