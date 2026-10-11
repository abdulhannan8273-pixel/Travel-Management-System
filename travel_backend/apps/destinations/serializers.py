from rest_framework import serializers
from .models import Destination, DestinationImage, Attraction
from apps.locations.serializers import (CountrySerializer, StateSerializer,CitySerializer)
from apps.locations.models import Country, State, City


class DestinationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationImage
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

class AttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction
        fields = "__all__"
        read_only_fields = ["id", "created_at",]

class DestinationSerializer(serializers.ModelSerializer):
    gallery = DestinationImageSerializer(many=True, read_only=True)
    attractions = AttractionSerializer(many=True, read_only=True)
   
   # GET response
    country_details = CountrySerializer(source="country", read_only=True)
    state_details = StateSerializer(source="state", read_only=True)
    city_details = CitySerializer(source="city", read_only=True)

    # POST/PUT request
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = Destination
        fields = "__all__"

class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith(".csv"):
            raise serializers.ValidationError(
                "Only CSV files are allowed."
            )
        return value