from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (DestinationViewSet, DestinationImageViewSet, AttractionViewSet, DestinationCSVImportView)

router = DefaultRouter()

router.register(r'destinations', DestinationViewSet, basename='destination')
router.register(r'destination-images', DestinationImageViewSet, basename='destination-image')
router.register(r'attractions', AttractionViewSet, basename='attraction')

urlpatterns = [
    path(
        "import-destinations/",
        DestinationCSVImportView.as_view(),
        name="import-destinations",
    ),
] + router.urls