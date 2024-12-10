from django.urls import path

from . import views

urlpatterns = [
    path(
        "search-profiles/",
        views.SearchProfileListView.as_view(),
        name="search_profiles",
    ),
]
