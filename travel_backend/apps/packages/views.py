from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Package, PackageImage
from .serializers import PackageSerializer, PackageImageSerializer
from apps.destinations.permissions import IsAdminOrReadOnly


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.select_related("Destination").prefetch_related("gallery").all()
    serializer_class = PackageSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = [
        "Destination",
        "is_featured",
        "is_active",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "price",
        "duration",
        "rating",
        "created_at",
    ]

    def _list_response(self, request, queryset):
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page if page is not None else queryset, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def popular(self, request):
        """Featured, active packages — newest first."""
        queryset = self.get_queryset().filter(is_active=True, is_featured=True).order_by("-created_at")
        return self._list_response(request, queryset)

    @action(detail=False, methods=["get"])
    def recommended(self, request):
        """Active packages sorted by rating (highest first)."""
        queryset = self.get_queryset().filter(is_active=True).order_by("-rating", "-created_at")
        return self._list_response(request, queryset)

    @action(detail=False, methods=["get"])
    def search(self, request):
        """Search active packages by name/description via ?q=keyword."""
        query = request.query_params.get("q", "").strip()
        queryset = self.get_queryset().filter(is_active=True)
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return self._list_response(request, queryset)


class PackageImageViewSet(viewsets.ModelViewSet):
    queryset = PackageImage.objects.select_related("package").all()
    serializer_class = PackageImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["package"]