from rest_framework.routers import DefaultRouter

from .views import (
    AirlineViewSet,
    AirportViewSet,
    FlightViewSet,
    FlightBookingViewSet,
)

router = DefaultRouter()

router.register(r"airlines", AirlineViewSet, basename="airline")
router.register(r"airports", AirportViewSet, basename="airport")
router.register(r"flights", FlightViewSet, basename="flight")
router.register(r"flight-bookings", FlightBookingViewSet, basename="flight-booking")
urlpatterns = router.urls