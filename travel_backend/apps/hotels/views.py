from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsAdminOrReadOnly
from .models import HotelImage
from .serializers import HotelImageSerializer


from .models import (
    Hotel,
    Room,
    HotelImage,
    HotelAmenity,
    HotelPolicy,
    HotelBooking,
)

from .serializers import (
    HotelSerializer,
    RoomSerializer,
    HotelImageSerializer,
    HotelAmenitySerializer,
    HotelPolicySerializer,
    HotelBookingSerializer,
)

#----------------------------hotel viewset------------------------------------------------------------------------------------------------------------

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.prefetch_related("reviews")
    serializer_class = HotelSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "destination",
        "star_rating",
        "is_featured",
    ]

    search_fields = [
        "name",
        "address",
    ]

    ordering_fields = [
        "price_per_night",
        "star_rating",
        "created_at",
    ]

#----------------------------room viewset------------------------------------------------------------------------------------------------------------

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related("hotel")
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "hotel",
        "room_type",
        "is_available",
    ]

    search_fields = [
        "room_type",
    ]

    ordering_fields = [
        "price_per_night",
        "capacity",
        "created_at",
    ]

#----------------------------hotel image viewset------------------------------------------------------------------------------------------------------------


class HotelImageViewSet(viewsets.ModelViewSet):
    queryset = HotelImage.objects.select_related("hotel")
    serializer_class = HotelImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_fields = [
        "hotel",
        "is_cover",
    ]

    ordering_fields = [
        "created_at",
    ]

#----------------------------hotel amenity viewset------------------------------------------------------------------------------------------------------------

class HotelAmenityViewSet(viewsets.ModelViewSet):
    queryset = HotelAmenity.objects.select_related("hotel")
    serializer_class = HotelAmenitySerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "hotel",
    ]

    search_fields = [
        "name",
    ]

    ordering_fields = [
        "name",
    ]

#----------------------------hotel policy viewset------------------------------------------------------------------------------------------------------------

class HotelPolicyViewSet(viewsets.ModelViewSet):
    queryset = HotelPolicy.objects.select_related("hotel")
    serializer_class = HotelPolicySerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "hotel",
    ]

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "title",
    ]


#----------------------------hotel booking viewset------------------------------------------------------------------------------------------------------------


class HotelBookingViewSet(viewsets.ModelViewSet):
    serializer_class = HotelBookingSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["booking_status", "hotel"]
    ordering_fields = ["created_at", "check_in_date"]

    def get_queryset(self):
        user = self.request.user
        qs = HotelBooking.objects.select_related("user", "hotel", "room")
        if user.is_staff:
            return qs.order_by("-created_at")
        return qs.filter(user=user).order_by("-created_at")

    @action(detail=False, methods=["get"])
    def my_bookings(self, request):
        bookings = self.get_queryset()
        serializer = self.get_serializer(bookings, many=True)
        return Response({"success": True, "count": bookings.count(), "data": serializer.data})

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = self.get_object()

        if booking.booking_status == "cancelled":
            return Response(
                {"success": False, "message": "Booking is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if booking.booking_status == "completed":
            return Response(
                {"success": False, "message": "Completed booking cannot be cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking.room.available_rooms += booking.number_of_rooms
        booking.room.save(update_fields=["available_rooms"])

        booking.booking_status = "cancelled"
        booking.save(update_fields=["booking_status"])

        return Response({"success": True, "message": "Booking cancelled successfully."})