from django.db.models import Q, Count
from django.db.models.functions import Lower
from django.utils import timezone
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from apps.destinations.models import Destination
from apps.destinations.serializers import DestinationSerializer
from apps.packages.models import Package
from apps.packages.serializers import PackageSerializer
from apps.hotels.models import Hotel
from apps.hotels.serializers import HotelSerializer

from .models import SearchLog

MIN_QUERY_LENGTH = 2
DEFAULT_LIMIT = 5
VALID_TYPES = {"all", "destinations", "packages", "hotels"}


class SearchView(APIView):
    """GET /api/search/?q=keyword&type=all&limit=5

    type: all (default) | destinations | packages | hotels
    A real, user-submitted search — logged for the 'popular searches' report.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        search_type = request.query_params.get("type", "all").lower()
        limit = min(int(request.query_params.get("limit", DEFAULT_LIMIT)), 50)

        if search_type not in VALID_TYPES:
            return Response(
                {"success": False, "message": f"type must be one of {sorted(VALID_TYPES)}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(query) < MIN_QUERY_LENGTH:
            return Response(
                {"success": False, "message": f"Query must be at least {MIN_QUERY_LENGTH} characters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        results = {}

        if search_type in ("all", "destinations"):
            destinations = Destination.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )[:limit]
            results["destinations"] = DestinationSerializer(destinations, many=True).data

        if search_type in ("all", "packages"):
            packages = Package.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query), is_active=True
            )[:limit]
            results["packages"] = PackageSerializer(packages, many=True).data

        if search_type in ("all", "hotels"):
            hotels = Hotel.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query) | Q(address__icontains=query)
            )[:limit]
            results["hotels"] = HotelSerializer(hotels, many=True).data

        SearchLog.objects.create(
            query=query,
            user=request.user if request.user.is_authenticated else None,
        )

        total_count = sum(len(v) for v in results.values())

        return Response(
            {
                "success": True,
                "query": query,
                "total_count": total_count,
                "results": results,
            },
            status=status.HTTP_200_OK,
        )


class SearchSuggestionsView(APIView):
    """GET /api/search/suggestions/?q=partial

    Lightweight autocomplete — small payload, not logged (called on every keystroke)."""
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        if len(query) < 1:
            return Response({"success": True, "suggestions": []}, status=status.HTTP_200_OK)

        suggestions = []

        for dest in Destination.objects.filter(name__icontains=query)[:5]:
            suggestions.append({"id": dest.id, "name": dest.name, "type": "destination"})

        for pkg in Package.objects.filter(name__icontains=query, is_active=True)[:5]:
            suggestions.append({"id": pkg.id, "name": pkg.name, "type": "package"})

        for hotel in Hotel.objects.filter(name__icontains=query)[:5]:
            suggestions.append({"id": hotel.id, "name": hotel.name, "type": "hotel"})

        return Response({"success": True, "suggestions": suggestions}, status=status.HTTP_200_OK)


class SearchPopularView(APIView):
    """GET /api/search/popular/?days=30&limit=10

    Most frequently searched terms in the last N days (default 30)."""
    permission_classes = [AllowAny]

    def get(self, request):
        days = int(request.query_params.get("days", 30))
        limit = min(int(request.query_params.get("limit", 10)), 50)

        since = timezone.now() - timedelta(days=days)

        popular = (
            SearchLog.objects.filter(created_at__gte=since)
            .annotate(query_lower=Lower("query"))
            .values("query_lower")
            .annotate(count=Count("id"))
            .order_by("-count")[:limit]
        )

        return Response(
            {
                "success": True,
                "days": days,
                "popular_searches": [
                    {"query": row["query_lower"], "count": row["count"]} for row in popular
                ],
            },
            status=status.HTTP_200_OK,
        )
    