from django.conf import settings

from adhocracy4 import emails as a4_emails


# Better use the Email class from adhocracy4.emails instead of this one directly
class Email(a4_emails.Email):
    """Email base class with a configurable default language."""

    fallback_language = "en"

    def get_languages(self, receiver):
        return [settings.DEFAULT_LANGUAGE, self.fallback_language]
