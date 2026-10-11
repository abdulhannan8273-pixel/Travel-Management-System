from rest_framework import serializers
from .models import Package, PackageImage
from apps.destinations.models import Destination
from apps.destinations.serializers import DestinationSerializer


class PackageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageImage
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class PackageSerializer(serializers.ModelSerializer):
    gallery = PackageImageSerializer(many=True, read_only=True)

    # GET response
    destination_details = DestinationSerializer(source="Destination", read_only=True)

    # POST/PUT request
    Destination = serializers.PrimaryKeyRelatedField(queryset=Destination.objects.all())

    class Meta:
        model = Package
        fields = "__all__"
        read_only_fields = ["slug", "rating"]