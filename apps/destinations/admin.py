from django.contrib import admin

# Register your models here.
from .models import Destination, DestinationImage, Attraction

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "country", "state", "city", "price", "rating", "is_featured", "is_active",
        )
    
    list_filter = (
        "country", "state", "city", "is_featured", "is_active",
        )
    
    search_fields = (
        "name",
        "country__name",
        "state__name",
        "city__name",
    )


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "destination", "is_active",
    )

    list_filter = (
        "destination", "is_active",
    )

    search_fields = (
        "name", "destination__name",
    )

@admin.register(DestinationImage)
class DestinationImageAdmin(admin.ModelAdmin):
    list_display = (
        "id", "destination", "created_at",
    )

    list_filter = (
        "destination",
    )

    search_fields = (
        "destination__name",
    )