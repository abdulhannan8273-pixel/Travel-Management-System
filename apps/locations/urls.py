from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CountryViewSet,
    StateViewSet,
    CityViewSet,
    CountryCSVImportView,
    StateCSVImportView,
    CityCSVImportView,
)
router = DefaultRouter()

router.register("countries", CountryViewSet, basename="countries")
router.register("states", StateViewSet, basename="states")
router.register("cities", CityViewSet, basename="cities")

urlpatterns = [
    path(
        "import-countries/",
        CountryCSVImportView.as_view(),
        name="import-countries",
    ),

    path(
    "import-states/",
    StateCSVImportView.as_view(),
    name="import-states",
    ),

    path(
    "import-cities/",
    CityCSVImportView.as_view(),
    name="import-cities",
    ),
]

urlpatterns += router.urls