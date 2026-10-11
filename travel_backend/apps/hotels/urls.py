from rest_framework.routers import DefaultRouter
from .views import (
    HotelViewSet,
    RoomViewSet,
    HotelImageViewSet,
    HotelAmenityViewSet,
    HotelPolicyViewSet,
)

router = DefaultRouter()

router.register(r"hotels", HotelViewSet, basename="hotel")
router.register(r"rooms", RoomViewSet, basename="room")
router.register(r"hotel-images", HotelImageViewSet, basename="hotel-image")
router.register(r"hotel-amenities", HotelAmenityViewSet, basename="hotel-amenity")
router.register(r"hotel-policies", HotelPolicyViewSet, basename="hotel-policy")

urlpatterns = router.urls