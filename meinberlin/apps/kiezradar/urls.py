from django.urls import path

from . import views

urlpatterns = [
    path(
        "kiezradar/",
        views.KiezRadarView.as_view(),
        name="kiezradar_filters",
    ),
    path(
        "kiezradar/<int:id>/",
        views.KiezRadarView.as_view(),
        name="kiezradar_edit",
    ),
    path(
        "kiezradar/new/",
        views.KiezRadarView.as_view(),
        name="kiezradar_new",
    ),
    path(
        "search-profiles/",
        views.SearchProfileListView.as_view(),
        name="search_profiles",
    ),
]
