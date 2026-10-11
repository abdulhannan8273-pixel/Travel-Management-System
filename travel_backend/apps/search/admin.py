from django.contrib import admin
from .models import SearchLog


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ("query", "user", "created_at")
    search_fields = ("query",)
    readonly_fields = ("query", "user", "created_at")
    