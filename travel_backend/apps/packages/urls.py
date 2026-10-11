from rest_framework.routers import DefaultRouter
from .views import PackageViewSet, PackageImageViewSet

router = DefaultRouter()
router.register(r"packages", PackageViewSet, basename="package")
router.register(r"package-images", PackageImageViewSet, basename="package-image")

urlpatterns = router.urls