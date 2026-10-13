from rest_framework.routers import DefaultRouter
from .views import UploadedFileViewSet

router = DefaultRouter()
router.register(r"uploads", UploadedFileViewSet, basename="upload")

urlpatterns = router.urls