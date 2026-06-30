from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, StateViewSet, CityViewSet

router = DefaultRouter()

router.register("countries", CountryViewSet, basename="countries")
router.register("states", StateViewSet, basename="states")
router.register("cities", CityViewSet, basename="cities")

urlpatterns = router.urls