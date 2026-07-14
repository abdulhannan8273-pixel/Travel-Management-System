from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import IsAdminOrReadOnly
from .models import Airline, Airport, Flight, FlightBooking
from .serializers import (
    AirlineSerializer,
    AirportSerializer,
    FlightSerializer,
    FlightBookingSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status



class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "country",
        "is_active",
    ]

    search_fields = [
        "name",
        "code",
        "country",
    ]

    ordering_fields = [
        "name",
        "created_at",
    ]


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "city",
        "country",
    ]

    search_fields = [
        "name",
        "code",
        "city",
        "country",
    ]

    ordering_fields = [
        "name",
        "city",
        "created_at",
    ]


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related(
        "airline",
        "source_airport",
        "destination_airport",
    )

    serializer_class = FlightSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "airline",
        "flight_class",
        "status",
        "source_airport",
        "destination_airport",
        "is_active",
    ]

    search_fields = [
        "flight_number",
        "airline__name",
        "source_airport__city",
        "destination_airport__city",
    ]

    ordering_fields = [
        "departure_time",
        "arrival_time",
        "price",
        "created_at",
    ]


class FlightBookingViewSet(viewsets.ModelViewSet):
    queryset = FlightBooking.objects.select_related("user", "flight")
    serializer_class = FlightBookingSerializer
    permission_classes = [IsAuthenticated]

    ...

    def get_queryset(self):
        if self.request.user.is_staff:
            return FlightBooking.objects.select_related(
                "user",
                "flight"
            )

        return FlightBooking.objects.select_related(
            "user",
            "flight"
        ).filter(user=self.request.user)

    @action(detail=True, methods=["patch"])
    def cancel(self, request, pk=None):
        booking = self.get_object()

        if booking.status == "cancelled":
            return Response(
                {"message": "Booking is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = "cancelled"

        booking.flight.available_seats += booking.passengers
        booking.flight.save()

        booking.save()

        return Response(
            {"message": "Booking cancelled successfully."}
        )