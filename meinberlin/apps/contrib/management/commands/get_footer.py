from pathlib import Path

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        footer_url = hasattr(settings, "BERLIN_FOOTER_URL")
        footer_filename = hasattr(settings, "BERLIN_FOOTER_FILENAME")
        if footer_url and footer_filename:
            filepath = Path(settings.MEDIA_ROOT) / settings.BERLIN_FOOTER_FILENAME
            try:
                response = requests.get(settings.BERLIN_FOOTER_URL, timeout=2.0)
                filepath.write_bytes(response.content)
                # update cache
                footer = filepath.read_text()
                cache.set("footer", footer)
                self.stdout.write(
                    "Succeeded downloading footer: '%s'." % footer_filename
                )
            except (requests.ConnectTimeout, requests.HTTPError, requests.Timeout) as e:
                self.stdout.write(
                    self.style.ERROR("Connection error downloading footer: '%s'." % e)
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR("Error downloading footer: '%s'." % e)
                )
        else:
            self.stdout.write(
                self.style.ERROR(
                    "Error downloading footer: BERLIN_FOOTER_URL"
                    " is not set. Add it to your settings."
                )
            )
