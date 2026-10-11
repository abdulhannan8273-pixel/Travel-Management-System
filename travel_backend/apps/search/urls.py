from django.urls import path
from .views import SearchView, SearchSuggestionsView, SearchPopularView

urlpatterns = [
    path("search/", SearchView.as_view(), name="search"),
    path("search/suggestions/", SearchSuggestionsView.as_view(), name="search-suggestions"),
    path("search/popular/", SearchPopularView.as_view(), name="search-popular"),
]