import pathlib

from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.test import override_settings

from meinberlin.apps.contrib.tasks import periodic_footer_update
from meinberlin.apps.contrib.templatetags.contrib_tags import get_external_footer


def test_get_footer_with_download(requests_mock):
    mock_footer = bytes("<p> berlin footer </p>", "utf-8")
    requests_mock.get(settings.BERLIN_FOOTER_URL, content=mock_footer)
    footer = cache.get("footer")
    assert footer is None
    footer_file = pathlib.Path(settings.MEDIA_ROOT, settings.BERLIN_FOOTER_FILENAME)
    if footer_file.exists():
        footer_file.unlink()
    footer = get_external_footer()
    footer = cache.get("footer")
    assert type(footer) is str
    assert footer == mock_footer.decode("utf-8")


@override_settings(BERLIN_FOOTER_URL="")
def test_task_footer_if_no_footer_url_in_settings():
    downloaded = periodic_footer_update()
    assert downloaded is False
    footer = cache.get("footer")
    assert footer is None


@override_settings(BERLIN_FOOTER_FILENAME="")
def test_task_footer_if_no_footer_filepath_in_settings():
    downloaded = periodic_footer_update()
    assert downloaded is False
    footer = cache.get("footer")
    assert footer is None


@override_settings(BERLIN_FOOTER_URL="", BERLIN_FOOTER_FILENAME="")
def test_task_footer_if_no_footer_settings():
    downloaded = periodic_footer_update()
    assert downloaded is False
    footer = cache.get("footer")
    assert footer is None

    # try with no footer settings at all
    del settings.BERLIN_FOOTER_URL
    del settings.BERLIN_FOOTER_FILENAME
    downloaded = periodic_footer_update()
    assert downloaded is False
    footer = cache.get("footer")


@override_settings(BERLIN_FOOTER_URL="", BERLIN_FOOTER_FILENAME="")
def test_command_get_footer_if_no_footer_settings():
    call_command("get_footer")
    assert cache.get("footer") is None

    # try with no footer settings at all
    del settings.BERLIN_FOOTER_URL
    del settings.BERLIN_FOOTER_FILENAME
    call_command("get_footer")
    assert cache.get("footer") is None


def test_command_get_footer(requests_mock):
    mock_footer = bytes("<p> berlin footer </p>", "utf-8")
    requests_mock.get(settings.BERLIN_FOOTER_URL, content=mock_footer)
    call_command("get_footer")
    footer = cache.get("footer")
    assert type(footer) is str
    assert footer == mock_footer.decode("utf-8")
