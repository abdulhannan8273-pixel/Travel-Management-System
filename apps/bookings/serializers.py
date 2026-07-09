from rest_framework import serializers
from .models import Booking
from datetime import date

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["id", "created_at", "user", "total_price", "status"]

    def validate_booking_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Booking date cannot be in the past.")
        return value
    
    def validate(self, attrs):
        user = self.context["request"].user

       
        destination = attrs.get("destination")
        booking_date = attrs.get("booking_date")

        if destination and booking_date:
            if Booking.objects.filter(
                user=user,
                destination=destination,
                booking_date=booking_date,
            ).exists():
                raise serializers.ValidationError(
                    "You already booked this destination on this date."
                )

        return attrs
    def validate_number_of_people(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "At least one traveler is required."
            )

        if value > 20:
            raise serializers.ValidationError(
                "A maximum of 20 travelers is allowed in a single booking."
            )

        return value
    
class BookingStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=["pending", "confirmed", "completed", "cancelled"]
    )