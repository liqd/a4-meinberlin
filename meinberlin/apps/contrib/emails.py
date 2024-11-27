from email.mime.image import MIMEImage

from django.conf import settings
from django.contrib.staticfiles import finders

from adhocracy4 import emails as a4_emails


class Email(a4_emails.Email):
    """Email base class with a configurable default language."""

    fallback_language = "en"

    def get_attachments(self):
        attachments = super().get_attachments()
        additional_files = [
            ("logo_berlin", "images/logo_berlin.svg"),
            ("logo_berlin_negative", "images/logo_berlin_negative.svg"),
            ("button_graphic", "images/email_button.png"),
        ]
        files = []
        for identifier, file in additional_files:
            filename = finders.find(file)
            if filename:
                if filename.endswith(".png"):
                    imagetype = "png"
                else:
                    imagetype = "svg+xml"

                with open(filename, "rb") as f:
                    image = MIMEImage(f.read(), imagetype)

                image.add_header("Content-ID", "<{}>".format(identifier))
                files.append(image)
        return attachments + files

    def get_languages(self, receiver):
        return [settings.DEFAULT_LANGUAGE, self.fallback_language]
