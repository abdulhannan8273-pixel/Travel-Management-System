from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AirportCSVImportView
from .views import (
    AirlineViewSet,
    AirportViewSet,
    FlightViewSet,
    FlightBookingViewSet,
    AirlineCSVImportView,
    AirportCSVImportView,
    FlightCSVImportView,
)
router = DefaultRouter()

router.register(r"airlines", AirlineViewSet, basename="airline")
router.register(r"airports", AirportViewSet, basename="airport")
router.register(r"flights", FlightViewSet, basename="flight")
router.register(r"flight-bookings", FlightBookingViewSet, basename="flight-booking",)

urlpatterns = [
    path(
        "import-airlines/",
        AirlineCSVImportView.as_view(),
        name="import-airlines",
    ),
    path(
        "import-airports/",
        AirportCSVImportView.as_view(),
        name="import-airports",
    ),
    path(
        "import-flights/",
        FlightCSVImportView.as_view(),
        name="import-flights",
    ),
] + router.urls