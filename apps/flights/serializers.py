from rest_framework import serializers
from .models import (Airline, Airport, Flight, FlightBooking,)
from decimal import Decimal
from django.utils import timezone
from apps.notifications.models import Notification

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class FlightSerializer(serializers.ModelSerializer):
    airline_name = serializers.CharField(
        source="airline.name",
        read_only=True
    )

    source_airport_name = serializers.CharField(
        source="source_airport.name",
        read_only=True
    )

    destination_airport_name = serializers.CharField(
        source="destination_airport.name",
        read_only=True
    )

    class Meta:
        model = Flight
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        source = attrs.get(
            "source_airport",
            getattr(self.instance, "source_airport", None)
        )

        destination = attrs.get(
            "destination_airport",
            getattr(self.instance, "destination_airport", None)
        )

        departure = attrs.get(
            "departure_time",
            getattr(self.instance, "departure_time", None)
        )

        arrival = attrs.get(
            "arrival_time",
            getattr(self.instance, "arrival_time", None)
        )

        total = attrs.get(
            "total_seats",
            getattr(self.instance, "total_seats", None)
        )

        available = attrs.get(
            "available_seats",
            getattr(self.instance, "available_seats", None)
        )

        if source == destination:
            raise serializers.ValidationError(
                "Source and destination airports cannot be the same."
            )

        if departure >= arrival:
            raise serializers.ValidationError(
                "Arrival time must be after departure time."
            )

        if available > total:
            raise serializers.ValidationError(
                "Available seats cannot exceed total seats."
            )

        return attrs


class FlightBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightBooking
        fields = "__all__"
        read_only_fields = [
            "id",
            "user",
            "total_price",
            "booking_date",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        flight = attrs["flight"]
        passengers = attrs["passengers"]

        # Flight cancelled
        if flight.status == "cancelled":
            raise serializers.ValidationError(
                "This flight has been cancelled."
            )

        # Flight already departed
        if flight.departure_time <= timezone.now():
            raise serializers.ValidationError(
                "This flight has already departed."
            )

        # Seat validation
        if passengers > flight.available_seats:
            raise serializers.ValidationError(
                "Not enough seats available."
            )

        return attrs

    def create(self, validated_data):
        flight = validated_data["flight"]
        passengers = validated_data["passengers"]

        validated_data["user"] = self.context["request"].user

        validated_data["total_price"] = (
            Decimal(flight.price) * passengers
        )

        flight.available_seats -= passengers
        flight.save()
        Notification.objects.create(
            user=validated_data["user"],
            title="Flight Booked",
            message=f"Flight {flight.flight_number} booked successfully."
            )
        return super().create(validated_data)
    
class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith(".csv"):
            raise serializers.ValidationError(
                "Only CSV files are allowed."
            )
        return value