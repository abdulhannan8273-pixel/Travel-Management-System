from django.contrib import admin
from .models import FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "package", "category", "order", "is_active")
    list_filter = ("category", "is_active", "package")
    search_fields = ("question", "answer")
    list_editable = ("order", "is_active")