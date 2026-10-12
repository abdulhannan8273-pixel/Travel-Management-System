from django.utils import timezone
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .models import NewsletterSubscriber
from .serializers import NewsletterSubscriberSerializer, EmailOnlySerializer


class NewsletterViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Admin-only list of subscribers. subscribe/unsubscribe are open actions below."""
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def subscribe(self, request):
        serializer = EmailOnlySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if not created and subscriber.is_active:
            return Response(
                {"success": False, "message": "This email is already subscribed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscriber.is_active = True
        subscriber.unsubscribed_at = None
        subscriber.save(update_fields=["is_active", "unsubscribed_at"])

        return Response({"success": True, "message": "Subscribed successfully."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def unsubscribe(self, request):
        serializer = EmailOnlySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            subscriber = NewsletterSubscriber.objects.get(email=email)
        except NewsletterSubscriber.DoesNotExist:
            return Response(
                {"success": False, "message": "This email is not subscribed."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not subscriber.is_active:
            return Response(
                {"success": False, "message": "This email is already unsubscribed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscriber.is_active = False
        subscriber.unsubscribed_at = timezone.now()
        subscriber.save(update_fields=["is_active", "unsubscribed_at"])

        return Response({"success": True, "message": "Unsubscribed successfully."}, status=status.HTTP_200_OK)