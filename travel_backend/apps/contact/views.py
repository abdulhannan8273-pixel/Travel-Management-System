from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactMessageViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Anyone can submit a message (create). Only admins can view/manage the inbox."""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAdminUser()]

    def perform_create(self, serializer):
        # Force is_resolved=False on creation, regardless of what a public
        # submitter sends — only an admin's later update should change it.
        serializer.save(is_resolved=False)