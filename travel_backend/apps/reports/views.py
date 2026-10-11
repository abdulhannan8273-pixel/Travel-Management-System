from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Report
from .serializers import ReportSerializer
from .analytics import (
    build_revenue_report,
    build_booking_report,
    build_user_report,
    build_package_report,
)

ANALYTICS_ACTIONS = ["revenue_report", "booking_report", "user_report", "package_report"]


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "report_type",
    ]

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "title",
    ]

    def get_permissions(self):
        if self.action in ANALYTICS_ACTIONS:
            return [IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self): # type: ignore[override]
        if self.request.user.is_staff:
            return Report.objects.select_related("generated_by")

        return Report.objects.select_related(
            "generated_by"
        ).filter(generated_by=self.request.user)

    @action(detail=False, methods=["get"])
    def revenue_report(self, request):
        """Admin-only. Optional ?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD."""
        return Response({"success": True, "data": build_revenue_report(request)}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def booking_report(self, request):
        """Admin-only. Optional ?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD."""
        return Response({"success": True, "data": build_booking_report(request)}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def user_report(self, request):
        """Admin-only. Optional ?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD."""
        return Response({"success": True, "data": build_user_report(request)}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def package_report(self, request):
        """Admin-only."""
        return Response({"success": True, "data": build_package_report(request)}, status=status.HTTP_200_OK)