from django.db.models import F
from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import BlogPost
from .serializers import BlogPostSerializer
from apps.destinations.permissions import IsAdminOrReadOnly


class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "is_published", "author"]
    search_fields = ["title", "content", "excerpt"]
    ordering_fields = ["created_at", "published_at", "views_count"]

    def get_queryset(self):
        qs = BlogPost.objects.select_related("author")
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return qs
        return qs.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_published:
            BlogPost.objects.filter(pk=instance.pk).update(views_count=F("views_count") + 1)
            instance.refresh_from_db(fields=["views_count"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)