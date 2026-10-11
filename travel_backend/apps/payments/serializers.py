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
            "amount",
            "payment_status",
            "paid_at",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        destination_booking = attrs.get("destination_booking")
        flight_booking = attrs.get("flight_booking")

        # Only one booking type allowed
        if destination_booking and flight_booking:
            raise serializers.ValidationError(
                "Select either destination booking or flight booking."
            )

        if not destination_booking and not flight_booking:
            raise serializers.ValidationError(
                "Booking is required."
            )

        # Destination Booking
        if destination_booking:

            if destination_booking.user != self.context["request"].user:
                raise serializers.ValidationError(
                    "This booking does not belong to you."
                )

            if destination_booking.status == "cancelled":
                raise serializers.ValidationError(
                    "Booking has already been cancelled."
                )

            queryset = Payment.objects.filter(
                destination_booking=destination_booking,
                payment_status="success",
            )

            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise serializers.ValidationError(
                    "Payment already completed."
                )

        # Flight Booking
        if flight_booking:

            if flight_booking.user != self.context["request"].user:
                raise serializers.ValidationError(
                    "This booking does not belong to you."
                )

            if flight_booking.booking_status == "cancelled":
                raise serializers.ValidationError(
                    "Booking has already been cancelled."
                )

            if Payment.objects.filter(
                flight_booking=flight_booking,
                payment_status="success",
            ).exists():
                raise serializers.ValidationError(
                    "Payment already completed."
                )

        return attrs

    def create(self, validated_data):

        validated_data["user"] = self.context["request"].user

        if validated_data.get("destination_booking"):
            validated_data["amount"] = (
                validated_data["destination_booking"].total_price
            )

        if validated_data.get("flight_booking"):
            validated_data["amount"] = (
                validated_data["flight_booking"].total_price
            )

        return super().create(validated_data)