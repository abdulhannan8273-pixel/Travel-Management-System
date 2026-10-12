from rest_framework import serializers
from .models import NewsletterSubscriber


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = "__all__"
        read_only_fields = ["id", "is_active", "subscribed_at", "unsubscribed_at"]


class EmailOnlySerializer(serializers.Serializer):
    email = serializers.EmailField()