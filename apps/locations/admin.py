from django.contrib import admin

# Register your models here.
from .models import Country, State, City

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "code", "is_active"
    )
    search_fields = ("name", "code")

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "code", "is_active"
    )
    list_filter = ("country",)
    search_fields = ("name",)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "state", "is_active"
    )
    list_filter = ("state", "is_active",)
    search_fields = ("name", "state_name",)