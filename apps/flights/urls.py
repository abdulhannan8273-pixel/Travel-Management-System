from rest_framework.routers import DefaultRouter

from .views import (
    AirlineViewSet,
    AirportViewSet,
    FlightViewSet,
)

router = DefaultRouter()

router.register(r"airlines", AirlineViewSet, basename="airline")
router.register(r"airports", AirportViewSet, basename="airport")
router.register(r"flights", FlightViewSet, basename="flight")

urlpatterns = router.urls