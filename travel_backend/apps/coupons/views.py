from django.db import models
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Coupon
from .serializers import CouponSerializer, ApplyCouponSerializer
from apps.destinations.permissions import IsAdminOrReadOnly


class CouponViewSet(viewsets.ModelViewSet):
    serializer_class = CouponSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_active", "discount_type"]
    search_fields = ["code", "description"]
    ordering_fields = ["created_at", "valid_until"]

    def get_queryset(self):
        qs = Coupon.objects.all()
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return qs
        # Non-staff only ever see coupons that are currently usable.
        now = timezone.now()
        qs = qs.filter(is_active=True, valid_from__lte=now, valid_until__gte=now)
        return qs.exclude(usage_limit__isnull=False, used_count__gte=models.F("usage_limit"))

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def apply(self, request):
        """Validate a coupon code against a given amount and return the discount."""
        serializer = ApplyCouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"].upper().strip()
        amount = serializer.validated_data["amount"]

        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return Response(
                {"success": False, "message": "Invalid coupon code."},
                status=status.HTTP_404_NOT_FOUND,
            )

        valid, message = coupon.is_valid_now()
        if not valid:
            return Response({"success": False, "message": message}, status=status.HTTP_400_BAD_REQUEST)

        discount, message = coupon.calculate_discount(amount)
        if discount is None:
            return Response({"success": False, "message": message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "success": True,
                "code": coupon.code,
                "discount_amount": discount,
                "final_amount": amount - discount,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def redeem(self, request, pk=None):
        """
        Call this once a booking/payment using this coupon is actually confirmed,
        to record that it was used (increments used_count). Not wired into the
        booking flow automatically yet — Booking/Payment don't reference Coupon.
        """
        coupon = self.get_object()
        valid, message = coupon.is_valid_now()
        if not valid:
            return Response({"success": False, "message": message}, status=status.HTTP_400_BAD_REQUEST)

        coupon.used_count += 1
        coupon.save(update_fields=["used_count"])
        return Response({"success": True, "used_count": coupon.used_count}, status=status.HTTP_200_OK)