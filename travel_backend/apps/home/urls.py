from django.urls import path
from .views import HomeAPIVies

urlpatterns = [
    path("", HomeAPIVies.as_view(), name="home")
]