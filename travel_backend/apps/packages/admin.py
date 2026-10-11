from django.contrib import admin
from .models import Package, PackageImage


class PackageImageInline(admin.TabularInline):
    model = PackageImage
    extra = 1


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "Destination", "price", "duration",
        "rating", "is_featured", "is_active",
    )

    list_filter = (
        "Destination", "is_featured", "is_active",
    )

    search_fields = (
        "name", "Destination__name",
    )

    prepopulated_fields = {"slug": ("name",)}
    inlines = [PackageImageInline]


@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    list_display = ("id", "package", "created_at")