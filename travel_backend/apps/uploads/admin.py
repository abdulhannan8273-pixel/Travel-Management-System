from django.contrib import admin
from .models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ("original_filename", "uploaded_by", "content_type", "file_size", "created_at")
    list_filter = ("content_type",)
    search_fields = ("original_filename",)
    readonly_fields = ("original_filename", "content_type", "file_size", "uploaded_by", "created_at")