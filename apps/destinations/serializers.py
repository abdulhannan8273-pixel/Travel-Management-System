from rest_framework import serializers
from .models import Destination, DestinationImage, Attraction
from apps.locations.serializers import (CountrySerializer, StateSerializer,CitySerializer)

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
    Country = CountrySerializer(read_only=True)
    state = StateSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Destination
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]













        