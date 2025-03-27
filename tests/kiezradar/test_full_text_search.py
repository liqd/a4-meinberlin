import pytest
from django.db import connection

from meinberlin.apps.kiezradar.matchers import full_text_search
from meinberlin.apps.kiezradar.matchers import sqlite_text_search
from meinberlin.apps.kiezradar.models import SearchProfile


@pytest.mark.django_db
def test_search_profiles(kiezradar_query_factory, search_profile_factory):
    profile1 = search_profile_factory(
        query=kiezradar_query_factory(text="Das ist Leipzig")
    )
    profile2 = search_profile_factory(
        query=kiezradar_query_factory(text="Das ist Berlin")
    )

    search_term = "Berlin Leipzig : Arts & Culture"
    search_term2 = "Berlin"
    search_term3 = "Arts and Culture"
    base_queryset = SearchProfile.objects.all()

    results = []
    results_leipzig = []
    results_empty = []

    if connection.vendor == "postgresql":
        results = full_text_search(search_term, base_queryset)
        results_leipzig = full_text_search(search_term2, base_queryset)
        results_empty = full_text_search(search_term3, base_queryset)

    else:
        results = sqlite_text_search(search_term, base_queryset)
        results_leipzig = sqlite_text_search(search_term2, base_queryset)
        results_empty = sqlite_text_search(search_term3, base_queryset)

    assert len(results) == 2
    assert profile1 in results
    assert profile2 in results
    assert profile2 in results_leipzig
    assert len(results_empty) == 0
