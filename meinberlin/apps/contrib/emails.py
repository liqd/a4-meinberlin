from django.conf import settings

from adhocracy4 import emails as a4_emails
from adhocracy4.projects.guest_users import is_guest_user


class Email(a4_emails.Email):
    """Email base class with a configurable default language.

    Also drops guest users from the recipient list centrally: guests use
    throwaway addresses and must never receive outbound mail. All meinBerlin
    email classes inherit from this base, so filtering here covers every
    outbound email (notifications, invites, newsletters, etc.).
    """

    fallback_language = "en"

    def get_languages(self, receiver):
        return [settings.DEFAULT_LANGUAGE, self.fallback_language]

    @staticmethod
    def _exclude_guest_users(receivers):
        """Return ``receivers`` without any guest users.

        Receivers may be ``User`` instances or plain email strings; strings
        (e.g. external notifications) are always kept.
        """
        return [
            receiver
            for receiver in receivers
            if not (hasattr(receiver, "email") and is_guest_user(receiver))
        ]

    def dispatch(self, object, *args, **kwargs):
        # Intercept receivers no matter which subclass defines get_receivers by
        # shadowing the bound method for the duration of the send.
        original_get_receivers = self.get_receivers
        self.get_receivers = lambda: self._exclude_guest_users(original_get_receivers())
        try:
            return super().dispatch(object, *args, **kwargs)
        finally:
            del self.get_receivers
