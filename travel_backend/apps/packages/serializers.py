from rest_framework import serializers
from .models import Package, PackageImage, PackageVideo
from apps.destinations.models import Destination
from apps.destinations.serializers import DestinationSerializer


class PackageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageImage
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class PackageVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageVideo
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


class PackageSerializer(serializers.ModelSerializer):
    gallery = PackageImageSerializer(many=True, read_only=True)
    videos = PackageVideoSerializer(many=True, read_only=True)
    faqs = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    # GET response
    destination_details = DestinationSerializer(source="Destination", read_only=True)

    # POST/PUT request
    Destination = serializers.PrimaryKeyRelatedField(queryset=Destination.objects.all())

    class Meta:
        model = Package
        fields = "__all__"
        read_only_fields = ["slug", "rating"]

    def get_faqs(self, obj):
        from apps.faqs.serializers import FAQSerializer
        return FAQSerializer(obj.faqs.filter(is_active=True), many=True).data

    def get_reviews(self, obj):
        from apps.reviews.serializers import ReviewSerializer
        return ReviewSerializer(obj.reviews.all(), many=True).data