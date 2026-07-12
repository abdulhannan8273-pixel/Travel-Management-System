from rest_framework import serializers
from .models import Airline, Airport, Flight


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