from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from apps.accounts.permissions import IsAdminOrReadOnly
from .models import Airline, Airport, Flight
from .serializers import (
    AirlineSerializer,
    AirportSerializer,
    FlightSerializer,
    CSVUploadSerializer,
)
from .csv_import import (
    import_airlines,
    import_airports,
    import_flights,
)
from rest_framework.permissions import IsAuthenticated
from .models import FlightBooking
from .serializers import FlightBookingSerializer
from rest_framework.decorators import action


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
    serializer_class = FlightBookingSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "booking_status",
        "payment_status",
        "flight",
    ]

    search_fields = [
        "flight__flight_number",
        "flight__airline__name",
    ]

    ordering_fields = [
        "booking_date",
        "created_at",
        "total_price",
    ]

    def get_queryset(self):
        if self.request.user.is_staff:
            return FlightBooking.objects.select_related(
                "user",
                "flight",
                "flight__airline",
            )

        return FlightBooking.objects.select_related(
            "user",
            "flight",
            "flight__airline",
        ).filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = self.get_object()

        # Sirf owner ya admin cancel kar sakta hai
        if (
            booking.user != request.user
            and not request.user.is_staff
        ):
            return Response(
                {
                    "success": False,
                    "message": "Permission denied."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Already cancelled
        if booking.booking_status == "cancelled":
            return Response(
                {
                    "success": False,
                    "message": "Booking is already cancelled."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Completed booking cancel nahi hogi
        if booking.booking_status == "completed":
            return Response(
                {
                    "success": False,
                    "message": "Completed booking cannot be cancelled."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Seats wapas add karo
        booking.flight.available_seats += booking.passengers
        booking.flight.save()

        booking.booking_status = "cancelled"
        booking.save()

        return Response(
            {
                "success": True,
                "message": "Booking cancelled successfully."
            },
            status=status.HTTP_200_OK,
        )
    @action(detail=False, methods=["get"])
    def my_bookings(self, request):
        bookings = (
            FlightBooking.objects
            .filter(user=request.user)
            .select_related(
                "flight",
                "flight__airline",
                "flight__source_airport",
                "flight__destination_airport",
            )
            .order_by("-booking_date")
        )

        serializer = self.get_serializer(bookings, many=True)

        return Response(
            {
                "success": True,
                "count": bookings.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {
                "success": False,
                "message": "Bookings cannot be deleted. Please cancel the booking instead."
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
    

class FlightCSVImportView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CSVUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        file = serializer.validated_data.get("file")

        if file is None:
            return Response(
                {"error": "File is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return import_flights(file)
    
class AirlineCSVImportView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CSVUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        validated_data = dict(serializer.validated_data)
        file = validated_data.get("file")

        if file is None:
            return Response(
                {"error": "File is required."},
                status=400,
            )

        return import_airlines(file)
    
class AirportCSVImportView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CSVUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        validated_data = dict(serializer.validated_data)
        file = validated_data.get("file")

        if file is None:
            return Response(
                {"error": "File is required."},
                status=400,
            )

        return import_airports(file)