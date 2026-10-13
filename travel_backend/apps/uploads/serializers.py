from rest_framework import serializers
from .models import UploadedFile

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
ALLOWED_CONTENT_TYPES = {
    "image/jpeg", "image/png", "image/webp", "image/gif", "image/svg+xml",
    "application/pdf",
}


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = "__all__"
        read_only_fields = [
            "id", "original_filename", "content_type", "file_size",
            "uploaded_by", "created_at",
        ]

    def validate_file(self, value):
        if value.size > MAX_FILE_SIZE_BYTES:
            raise serializers.ValidationError(
                f"File too large ({value.size} bytes). Max allowed is {MAX_FILE_SIZE_BYTES} bytes (10 MB)."
            )
        content_type = getattr(value, "content_type", "") or ""
        if content_type not in ALLOWED_CONTENT_TYPES:
            raise serializers.ValidationError(
                f"Unsupported file type '{content_type}'. Allowed: {sorted(ALLOWED_CONTENT_TYPES)}."
            )
        return value