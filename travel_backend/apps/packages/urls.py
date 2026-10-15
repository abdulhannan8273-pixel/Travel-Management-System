from rest_framework.routers import DefaultRouter
from .views import PackageViewSet, PackageImageViewSet, PackageVideoViewSet

router = DefaultRouter()
router.register(r"packages", PackageViewSet, basename="package")
router.register(r"package-images", PackageImageViewSet, basename="package-image")
router.register(r"package-videos", PackageVideoViewSet, basename="package-video")

urlpatterns = router.urls