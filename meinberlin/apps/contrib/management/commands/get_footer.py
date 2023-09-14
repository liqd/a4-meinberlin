import requests
from django.conf import settings
from django.core.cache import cache
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        if hasattr(settings, "BERLIN_FOOTER_URL") and settings.BERLIN_FOOTER_URL:
            filepath = settings.MEDIA_ROOT + "/landesfooter.inc"
            try:
                response = requests.get(settings.BERLIN_FOOTER_URL, timeout=2.0)
                with open(filepath, "wb") as f:
                    f.write(response.content)
                # clear cache
                cache.delete("footer")
                return False
            except (requests.ConnectTimeout, requests.HTTPError, requests.Timeout) as e:
                self.stdout.write(
                    self.style.ERROR('Error downloading footer: "%s".' % e)
                )
        else:
            self.stdout.write(
                self.style.ERROR(
                    "Error downloading footer: BERLIN_FOOTER_URL"
                    " is not set. Add it to your settings."
                )
            )
        # indicate error
        return True
