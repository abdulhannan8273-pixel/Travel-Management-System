from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = [
            "id",
            "user",
            "transaction_id",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        booking = attrs.get("booking")

        # During PATCH requests, booking isn't sent.
        if booking is None and self.instance:
            booking = self.instance.booking

        if Payment.objects.filter(
            booking=booking,
            payment_status="success"
        ).exclude(
            pk=self.instance.pk if self.instance else None
        ).exists():
            raise serializers.ValidationError(
                "Payment has already been completed for this booking."
            )

        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user

        # Automatically copy the booking amount
        validated_data["amount"] = validated_data["booking"].total_price

        return super().create(validated_data)