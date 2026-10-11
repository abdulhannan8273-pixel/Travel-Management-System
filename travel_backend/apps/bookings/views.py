from decimal import Decimal

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer, BookingStatusSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "status",
        "booking_date",
        "destination",
    ]

    search_fields = [
        "destination__name",
    ]
    ordering_fields = [
        "created_at",
        "booking_date",
        "total_price",
    ]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return (
                Booking.objects
                .select_related("user", "destination")
                .order_by("-created_at")
            )

        return (
            Booking.objects
            .select_related("destination")
            .filter(user=user)
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        destination = serializer.validated_data["destination"]
        people = serializer.validated_data["number_of_people"]

        total = Decimal(destination.price) * people

        serializer.save(
            user=self.request.user,
            total_price=total
        )

    @action(detail=True, methods=["patch"])
    def cancel(self, request, pk=None):
        booking = self.get_object()

        # Owner or admin check
        if booking.user != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to cancel this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Status validation
        if booking.status == "completed":
            return Response(
                {"detail": "Completed bookings cannot be cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if booking.status == "cancelled":
            return Response(
                {"detail": "Booking is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = "cancelled"
        booking.save()

        return Response(
            {
                "success": True,
                "message": "Booking cancelled successfully."
            },
            status=status.HTTP_200_OK,
        )
    
    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        booking = self.get_object()

        # Only admin can update booking status
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admins can update booking status."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = BookingStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data["status"]

        # Business rules
        if booking.status == "completed":
            return Response(
                {"detail": "Completed booking status cannot be changed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if booking.status == "cancelled":
            return Response(
                {"detail": "Cancelled booking status cannot be changed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = new_status
        booking.save()

        return Response(
            {
                "success": True,
                "message": "Booking status updated successfully.",
                "status": booking.status,
            },
            status=status.HTTP_200_OK,
        )