from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import FAQ
from .serializers import FAQSerializer
from apps.destinations.permissions import IsAdminOrReadOnly


class FAQViewSet(viewsets.ModelViewSet):
    serializer_class = FAQSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category", "is_active"]
    search_fields = ["question", "answer"]

    def get_queryset(self):
        qs = FAQ.objects.all()
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return qs
        return qs.filter(is_active=True)