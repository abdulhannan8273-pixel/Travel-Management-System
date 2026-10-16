from rest_framework import serializers
from apps.reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]

    def validate(self, attrs):
        # On a partial update (PATCH) a target field might not be resent —
        # fall back to the existing instance's value so validation still
        # sees the real, complete picture.
        instance = self.instance
        destination = attrs.get("destination", getattr(instance, "destination", None))
        package = attrs.get("package", getattr(instance, "package", None))
        hotel = attrs.get("hotel", getattr(instance, "hotel", None))

        targets_set = sum(1 for t in (destination, package, hotel) if t is not None)
        if targets_set != 1:
            raise serializers.ValidationError(
                "Provide exactly one of destination, package, or hotel."
            )

        request = self.context.get("request")
        user = getattr(request, "user", None)
        if user and user.is_authenticated:
            existing = Review.objects.filter(
                user=user, destination=destination, package=package, hotel=hotel
            )
            if instance:
                existing = existing.exclude(pk=instance.pk)
            if existing.exists():
                raise serializers.ValidationError("You have already reviewed this item.")

        return attrs