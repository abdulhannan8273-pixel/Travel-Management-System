from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UploadedFile
from .serializers import UploadedFileSerializer


class UploadedFileViewSet(viewsets.ModelViewSet):
    """
    POST /api/uploads/  (multipart, field name 'file') — upload
    DELETE /api/uploads/<id>/                           — delete

    A user can only see/delete their own uploads; staff can see/delete all.
    """
    serializer_class = UploadedFileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self):
        qs = UploadedFile.objects.select_related("uploaded_by")
        if self.request.user.is_staff:
            return qs
        return qs.filter(uploaded_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded = request.data.get("file")
        serializer.save(
            uploaded_by=request.user,
            original_filename=getattr(uploaded, "name", ""),
            content_type=getattr(uploaded, "content_type", ""),
            file_size=getattr(uploaded, "size", 0),
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)