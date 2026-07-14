from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "payment_status",
        "payment_method",
        "booking",
    ]

    search_fields = [
        "transaction_id",
        "booking__id",
    ]

    ordering_fields = [
        "amount",
        "created_at",
        "paid_at",
    ]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.select_related(
                "user",
                "booking"
            )

        return Payment.objects.select_related(
            "user",
            "booking"
        ).filter(user=self.request.user)