from rest_framework.routers import DefaultRouter
from .views import (DestinationViewSet, DestinationImageViewSet, AttractionViewSet,)

router = DefaultRouter()

router.register(r'destinations', DestinationViewSet, basename='destination')
router.register(r'destination-images', DestinationImageViewSet, basename='destination-image')
router.register(r'attractions', AttractionViewSet, basename='attraction')

urlpatterns = router.urls