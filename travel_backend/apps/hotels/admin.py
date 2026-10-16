from django.contrib import admin
from .models import (
    Hotel,
    Room,
    HotelImage,
    HotelAmenity,
    HotelPolicy,
    HotelBooking,
)

#----------------------------hotel admin------------------------------------------------------------------------------------------------------------
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "destination", "star_rating", "price_per_night", "available_rooms", "is_featured")
    list_filter = ("destination", "is_featured", "star_rating")
    search_fields = ("name", "address")

#----------------------------room admin------------------------------------------------------------------------------------------------------------
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("hotel", "room_type", "price_per_night", "available_rooms", "is_available")
    list_filter = ("room_type", "is_available")
    search_fields = ("hotel__name",)


admin.site.register(HotelImage)
admin.site.register(HotelAmenity)
admin.site.register(HotelPolicy)

#----------------------------hotel booking admin------------------------------------------------------------------------------------------------------------
@admin.register(HotelBooking)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "hotel", "room", "check_in_date", "check_out_date",
        "number_of_rooms", "total_price", "booking_status", "payment_status",
    )
    list_filter = ("booking_status", "payment_status")
    search_fields = ("user__email", "hotel__name")