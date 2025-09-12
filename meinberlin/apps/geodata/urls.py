from django.urls import path

from . import views

urlpatterns = [
    path("search", views.search_addresses, name="geodata-search-addresses"),
    path(
        "search-by-feature/<str:feature_id>/",
        views.get_address,
        name="geodata-get-address",
    ),
]
