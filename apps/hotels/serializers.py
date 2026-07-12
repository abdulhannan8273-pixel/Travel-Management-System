from rest_framework import serializers
from .models import (
    Hotel,
    Room,
    HotelImage,
    HotelAmenity,
    HotelPolicy,
)

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = "__all__"
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        hotel = attrs.get("hotel", getattr(self.instance, "hotel", None))
        is_cover = attrs.get("is_cover", getattr(self.instance, "is_cover", False))

        if is_cover:
            qs = HotelImage.objects.filter(
                hotel=hotel,
                is_cover=True
            )

            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError(
                    "This hotel already has a cover image."
                )

        return attrs

class HotelAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelAmenity
        fields = "__all__"
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        hotel = attrs.get("hotel", getattr(self.instance, "hotel", None))
        name = attrs.get("name", getattr(self.instance, "name", None))

        qs = HotelAmenity.objects.filter(
            hotel=hotel,
            name__iexact=name
        )

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "This amenity already exists for this hotel."
            )

        return attrs


class HotelPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelPolicy
        fields = "__all__"
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        hotel = attrs.get("hotel", getattr(self.instance, "hotel", None))
        title = attrs.get("title", getattr(self.instance, "title", None))

        qs = HotelPolicy.objects.filter(
            hotel=hotel,
            title__iexact=title
        )

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "This policy already exists for this hotel."
            )

        return attrs

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

class HotelSerializer(serializers.ModelSerializer):
    images = HotelImageSerializer(many=True, read_only=True)
    amenities = HotelAmenitySerializer(many=True, read_only=True)
    policies = HotelPolicySerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = "__all__"