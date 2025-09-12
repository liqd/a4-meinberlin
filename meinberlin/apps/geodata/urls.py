from django.urls import path

from . import views

urlpatterns = [
    path("search", views.search_addresses, name="geodata-search-addresses"),
]
