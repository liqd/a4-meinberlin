from django.urls import path

from . import views

urlpatterns = [
    path(
        "kiezauswahl/",
        views.KiezRadarView.as_view(),
        name="kiezradar_filters",
    ),
    path(
        "kiezauswahl/<int:id>/",
        views.KiezRadarView.as_view(),
        name="kiezradar_edit",
    ),
    path(
        "kiezauswahl/new/",
        views.KiezRadarView.as_view(),
        name="kiezradar_new",
    ),
    path(
        "search-profiles/",
        views.SearchProfileListView.as_view(),
        name="search_profiles",
    ),
]
