from django.urls import path
from .views import DestinationCreateView

urlpatterns = [path("created/", DestinationCreateView.as_view(),  name="destinatin-create")]