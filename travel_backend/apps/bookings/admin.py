from django.contrib import admin

# Register your models here.
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
   list_display = ("id", "user", "destination", "package", "booking_date", "number_of_people", "total_price", "status", "created_at",) 
   list_filter = ("status", "booking_date",)
   search_fields = ("user__username", "destination__name", "package__name",)