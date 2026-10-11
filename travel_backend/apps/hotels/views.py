from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import (
    Hotel,
    Room,
    HotelImage,
    HotelAmenity,
    HotelPolicy,
)

from .serializers import (
    HotelSerializer,
    RoomSerializer,
    HotelImageSerializer,
    HotelAmenitySerializer,
    HotelPolicySerializer,
)

from .permissions import IsAdminOrReadOnly
from .models import HotelImage
from .serializers import HotelImageSerializer

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
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