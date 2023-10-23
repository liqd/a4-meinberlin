import logging
from pathlib import Path

import requests
from celery import shared_task
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


def download_footer(footer_url, filepath) -> bool:
    """Downloads footer from a link specified in the settings.

    Returns:
        A boolean indicating whether download was succeeded.
    """
    try:
        response = requests.get(footer_url, timeout=2.0)
        filepath.write_bytes(response.content)
    except (requests.ConnectTimeout, requests.HTTPError, requests.Timeout) as e:
        logger.error("Connection error downloading footer: '%s'." % e)
        return False
    except Exception as e:
        logger.error("Error downloading footer: '%s'." % e)
        return False
    else:
        return True


@shared_task
def periodic_footer_update() -> bool:
    """The task is called inline by contrib templatetag
    'get_external_footer'.

    It can be scheduled in django admin for periodic
    footer downloading. See docs/celerybeat.md

    Returns:
        A boolean indicating whether the download succeeded
    """
    footer_url = hasattr(settings, "BERLIN_FOOTER_URL")
    footer_filename = hasattr(settings, "BERLIN_FOOTER_FILENAME")
    downloaded = False
    if footer_url and footer_filename:
        filepath = Path(settings.MEDIA_ROOT) / settings.BERLIN_FOOTER_FILENAME
        downloaded = download_footer(settings.BERLIN_FOOTER_URL, filepath)
        if downloaded:  # set footer in the cache
            cache.set("footer", filepath.read_text())
    else:
        logger.error(
            "Error downloading footer: BERLIN_FOOTER_URL"
            " is not set. Add it to your settings."
        )
    return downloaded
