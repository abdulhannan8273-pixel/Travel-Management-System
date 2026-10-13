from django.conf import settings
from django.db import models


class UploadedFile(models.Model):
    """
    Generic standalone file upload — for cases where the frontend needs to
    upload an image/file BEFORE the parent object (a package, a blog post,
    etc.) exists yet. Most other apps (packages, hotels, destinations) still
    have their own dedicated image fields/models for normal use.
    """
    file = models.FileField(upload_to="uploads/%Y/%m/")
    original_filename = models.CharField(max_length=255, blank=True)
    content_type = models.CharField(max_length=100, blank=True)
    file_size = models.PositiveIntegerField(default=0, help_text="Size in bytes.")

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_files",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "uploaded_files"
        ordering = ["-created_at"]

    def __str__(self):
        return self.original_filename or self.file.name