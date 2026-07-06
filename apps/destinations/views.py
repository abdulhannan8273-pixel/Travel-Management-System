from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from django.db.models.query import QuerySet
from .models import Destination, DestinationImage, Attraction
from .serializers import (DestinationSerializer, DestinationImageSerializer, AttractionSerializer,)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = [
        "country",
        "state",
        "city",
        "is_featured",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "price",
        "rating",
        "created_at",
    ]

    def get_queryset(self):
        queryset = Destination.objects.all()

        request = self.request
        params = request.query_params if isinstance(request, Request) else request.GET

        min_price = params.get("min_price")
        max_price = params.get("max_price")
        min_rating = params.get("min_rating")

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)

        return queryset

class DestinationImageViewSet(viewsets.ModelViewSet):
    queryset = DestinationImage.objects.all()
    serializer_class = DestinationImageSerializer
    permission_classes = [IsAuthenticated]


class AttractionViewSet(viewsets.ModelViewSet):
    queryset = Attraction.objects.all()
    serializer_class = AttractionSerializer
    permission_classes = [IsAuthenticated]