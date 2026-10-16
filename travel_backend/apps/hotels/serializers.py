from decimal import Decimal
from rest_framework import serializers
from .models import (
    Hotel,
    Room,
    HotelImage,
    HotelAmenity,
    HotelPolicy,
    HotelBooking,
)

#----------------------------hotel image serializer------------------------------------------------------------------------------------------------------------

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

#----------------------------hotel amenity serializer------------------------------------------------------------------------------------------------------------

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
#----------------------------hotel policy serializer------------------------------------------------------------------------------------------------------------

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
#----------------------------room serializer------------------------------------------------------------------------------------------------------------
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

#----------------------------hotel serializer-----------------------------------------

class HotelSerializer(serializers.ModelSerializer):
    images = HotelImageSerializer(many=True, read_only=True)
    amenities = HotelAmenitySerializer(many=True, read_only=True)
    policies = HotelPolicySerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = "__all__"

    def get_reviews(self, obj):
        from apps.reviews.serializers import ReviewSerializer
        return ReviewSerializer(obj.reviews.all(), many=True).data

#----------------------------hotel booking serializer------------------------------------------------------------------------------------------------------------

class HotelBookingSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source="hotel.name", read_only=True)
    room_type = serializers.CharField(source="room.room_type", read_only=True)

    class Meta:
        model = HotelBooking
        fields = "__all__"
        read_only_fields = [
            "id",
            "user",
            "total_price",
            "booking_status",
            "payment_status",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        room = attrs["room"]
        hotel = attrs["hotel"]
        check_in = attrs["check_in_date"]
        check_out = attrs["check_out_date"]
        number_of_rooms = attrs.get("number_of_rooms", 1)

        if room.hotel_id != hotel.id:
            raise serializers.ValidationError("This room does not belong to the selected hotel.")

        if check_out <= check_in:
            raise serializers.ValidationError("check_out_date must be after check_in_date.")

        if not room.is_available:
            raise serializers.ValidationError("This room type is not currently available.")

        if number_of_rooms > room.available_rooms:
            raise serializers.ValidationError(
                f"Only {room.available_rooms} room(s) of this type are available."
            )

        return attrs

    def create(self, validated_data):
        from apps.notifications.models import Notification

        room = validated_data["room"]
        check_in = validated_data["check_in_date"]
        check_out = validated_data["check_out_date"]
        number_of_rooms = validated_data.get("number_of_rooms", 1)
        nights = (check_out - check_in).days

        validated_data["user"] = self.context["request"].user
        validated_data["total_price"] = Decimal(room.price_per_night) * nights * number_of_rooms

        room.available_rooms -= number_of_rooms
        room.save(update_fields=["available_rooms"])

        booking = super().create(validated_data)

        Notification.objects.create(
            user=booking.user,
            title="Hotel Booked",
            message=f"Your booking at {booking.hotel.name} ({check_in} to {check_out}) has been created.",
        )

        return booking