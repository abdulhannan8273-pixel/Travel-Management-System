from django.utils import timezone

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from .models import Payment
from .serializers import PaymentSerializer
from apps.notifications.models import Notification

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related(
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

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset

        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def success(self, request, pk=None):
        payment = self.get_object()

        if payment.payment_status == "success":
            Notification.objects.create(
                user=payment.user,
                title="Payment Successful",
                message=f"Your payment ({payment.transaction_id}) was completed successfully."
                )
            return Response(
                {
                    "success": False,
                    "message": "Payment already completed."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment.payment_status = "success"
        payment.paid_at = timezone.now()
        payment.save(update_fields=["payment_status", "paid_at"])

        if payment.destination_booking:
            payment.destination_booking.status = "confirmed"
            payment.destination_booking.save(
                update_fields=["status"]
            )

        if payment.flight_booking:
            payment.flight_booking.booking_status = "confirmed"
            payment.flight_booking.payment_status = True
            payment.flight_booking.save(
                update_fields=[
                    "booking_status",
                    "payment_status",
                ]
            )

        return Response(
            {
                "success": True,
                "message": "Payment completed successfully."
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def failed(self, request, pk=None):
        payment = self.get_object()

        if payment.payment_status == "failed":
            Notification.objects.create(
                user=payment.user,
                title="Payment Failed",
                message=f"Your payment ({payment.transaction_id}) has failed."
    )
            return Response(
                {
                    "success": False,
                    "message": "Payment already marked as failed."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment.payment_status = "failed"
        payment.save(update_fields=["payment_status"])

        if payment.flight_booking:
            payment.flight_booking.booking_status = "cancelled"
            payment.flight_booking.payment_status = False
            payment.flight_booking.save(
                update_fields=[
                    "booking_status",
                    "payment_status",
                ]
            )

        return Response(
            {
                "success": True,
                "message": "Payment marked as failed."
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def retry(self, request, pk=None):
        payment = self.get_object()

        if payment.payment_status != "failed":
            return Response(
                {
                    "success": False,
                    "message": "Only failed payments can be retried."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment.payment_status = "pending"
        payment.save(update_fields=["payment_status"])

        return Response(
            {
                "success": True,
                "message": "Payment is ready to retry."
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def refund(self, request, pk=None):
        payment = self.get_object()

        if payment.payment_status != "success":
            Notification.objects.create(
                user=payment.user,
                title="Payment Refunded",
                message=f"Your payment ({payment.transaction_id}) has been refunded."
                )
            return Response(
                {
                    "success": False,
                    "message": "Only successful payments can be refunded."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment.payment_status = "refunded"
        payment.paid_at = None
        payment.save(
            update_fields=[
                "payment_status",
                "paid_at",
            ]
        )

        if payment.destination_booking:
            payment.destination_booking.status = "cancelled"
            payment.destination_booking.save(
                update_fields=["status"]
            )

        if payment.flight_booking:
            flight_booking = payment.flight_booking

            flight_booking.booking_status = "cancelled"
            flight_booking.payment_status = False

            flight_booking.flight.available_seats += (
                flight_booking.passengers
            )

            flight_booking.flight.save(
                update_fields=["available_seats"]
            )

            flight_booking.save(
                update_fields=[
                    "booking_status",
                    "payment_status",
                ]
            )

        return Response(
            {
                "success": True,
                "message": "Payment refunded successfully."
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def my_payments(self, request):
        payments = self.get_queryset()

        serializer = self.get_serializer(
            payments,
            many=True,
        )

        return Response(
            {
                "success": True,
                "count": payments.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )