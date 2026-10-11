import hmac
import hashlib
import json

from django.conf import settings
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend

from .models import Payment
from .serializers import PaymentSerializer
from .services import mark_payment_success, mark_payment_failed, mark_payment_refunded


class PaymentViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Payment] = Payment.objects.select_related(
        "user",
        "destination_booking",
        "flight_booking",
    )

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "payment_status",
        "payment_method",
    ]

    search_fields = [
        "transaction_id",
    ]

    ordering_fields = [
        "created_at",
        "amount",
    ]

    def get_queryset(self) -> QuerySet[Payment]:  # type: ignore[override]
        if self.request.user.is_staff:
            return self.queryset

        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def success(self, request, pk=None):
        payment = self.get_object()

        if not mark_payment_success(payment):
            return Response(
                {"success": False, "message": "Payment already completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"success": True, "message": "Payment completed successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def failed(self, request, pk=None):
        payment = self.get_object()

        if not mark_payment_failed(payment):
            return Response(
                {"success": False, "message": "Payment already marked as failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"success": True, "message": "Payment marked as failed."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def retry(self, request, pk=None):
        payment = self.get_object()

        if payment.payment_status != "failed":
            return Response(
                {"success": False, "message": "Only failed payments can be retried."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment.payment_status = "pending"
        payment.save(update_fields=["payment_status"])

        return Response(
            {"success": True, "message": "Payment is ready to retry."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def refund(self, request, pk=None):
        payment = self.get_object()

        if not mark_payment_refunded(payment):
            return Response(
                {"success": False, "message": "Only successful payments can be refunded."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"success": True, "message": "Payment refunded successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def my_payments(self, _request):
        payments = self.get_queryset()
        serializer = self.get_serializer(payments, many=True)

        return Response(
            {
                "success": True,
                "count": payments.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


@method_decorator(csrf_exempt, name="dispatch")
class RazorpayWebhookView(APIView):
    """
    Receives server-to-server payment status updates from Razorpay.

    Configure this URL in the Razorpay Dashboard -> Settings -> Webhooks,
    and set RAZORPAY_WEBHOOK_SECRET in your .env to the secret shown there.

    This endpoint is intentionally open (no login required) because Razorpay's
    servers call it directly, not a logged-in user. Security instead comes
    entirely from verifying the HMAC signature below.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if not settings.RAZORPAY_WEBHOOK_SECRET:
            return Response(
                {"success": False, "message": "Webhook secret not configured on server."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        signature = request.headers.get("X-Razorpay-Signature", "")
        body = request.body

        expected_signature = hmac.new(
            settings.RAZORPAY_WEBHOOK_SECRET.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(expected_signature, signature):
            return Response(
                {"success": False, "message": "Invalid webhook signature."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            payload = json.loads(body)
        except (ValueError, TypeError):
            return Response(
                {"success": False, "message": "Invalid JSON payload."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event = payload.get("event", "")
        entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
        razorpay_order_id = entity.get("order_id")
        razorpay_payment_id = entity.get("id")

        if not razorpay_order_id:
            return Response({"success": True, "message": "Event ignored."}, status=status.HTTP_200_OK)

        try:
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        except Payment.DoesNotExist:
            return Response(
                {"success": False, "message": "No matching payment found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if event == "payment.captured":
            mark_payment_success(payment, razorpay_payment_id=razorpay_payment_id)
        elif event == "payment.failed":
            mark_payment_failed(payment)
        elif event == "refund.processed":
            mark_payment_refunded(payment)

        return Response({"success": True}, status=status.HTTP_200_OK)