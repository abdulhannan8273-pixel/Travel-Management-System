from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Notification.objects.all()

        return Notification.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["patch"])
    def mark_read(self, request, pk=None):
        notification = self.get_object()

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return Response(
            {
                "success": True,
                "message": "Notification marked as read."
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["patch"])
    def mark_all_read(self, request):

        queryset = self.get_queryset().filter(
            is_read=False
        )

        queryset.update(is_read=True)

        return Response(
            {
                "success": True,
                "message": "All notifications marked as read."
            },
            status=status.HTTP_200_OK,
        )