from urllib.parse import urlparse

from allauth.account.views import LoginView
from django.utils.http import url_has_allowed_host_and_scheme


class CustomLoginView(LoginView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context.get("redirect_field_value"):
            return context

        referer = self.request.META.get("HTTP_REFERER", "")
        if not url_has_allowed_host_and_scheme(
            referer,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return context

        parsed = urlparse(referer)
        if parsed.path.startswith("/accounts/"):
            return context

        path = parsed.path
        if parsed.query:
            path = f"{path}?{parsed.query}"
        context["redirect_field_value"] = path
        return context
