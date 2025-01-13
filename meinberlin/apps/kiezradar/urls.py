from django.urls import path

from . import views

urlpatterns = [
    path(
        "kiezradar-filters/",
        views.KiezRadarListView.as_view(),
        name="kiezradar_filters",
    ),
    path(
        "kiezradar/new",
        views.KiezRadarCreateView.as_view(),
        name="kiezradar_create",
    ),
    path(
        "kiezradar/",
        views.KiezRadarDetailView.as_view(),
        name="kiezradar_detail",
    ),
    path(
        "search-profiles/",
        views.SearchProfileListView.as_view(),
        name="search_profiles",
    ),
]
