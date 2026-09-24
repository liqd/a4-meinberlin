from urllib.parse import urlparse

from allauth.account.views import LoginView
from allauth.account.views import SignupView
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import FormView
from guest_user.functions import maybe_create_guest_user

from .forms import GuestCreateForm


class HtmxAuthMixin:
    """Serve auth forms as fragments and close the modal via HX-Redirect.

    When a request comes from htmx (``HX-Request`` header) the view renders only
    the form fragment (``htmx_template_name``) instead of the full page. On a
    successful submit it answers with ``HX-Redirect`` so htmx performs a full
    page navigation (e.g. back to the page the modal was opened from) instead of
    swapping the redirected page into the modal.
    """

    htmx_template_name = None

    def _is_htmx(self):
        return self.request.headers.get("HX-Request") == "true"

    def get_template_names(self):
        if self._is_htmx() and self.htmx_template_name:
            return [self.htmx_template_name]
        return super().get_template_names()

    def form_valid(self, form):
        response = super().form_valid(form)
        if self._is_htmx():
            location = getattr(response, "url", None)
            if location is None:
                location = response.get("Location")
            if location:
                return HttpResponse(status=204, headers={"HX-Redirect": str(location)})
        return response


class GuestCreateView(HtmxAuthMixin, FormView):
    """Terms + captcha gate; on submit start a guest session and redirect back."""

    form_class = GuestCreateForm
    template_name = "meinberlin_users/guest_create.html"
    htmx_template_name = "meinberlin_users/guest_create_content.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        next_url = self.request.POST.get("next") or self.request.GET.get("next")
        return next_url or "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET.get("next", "")
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial["next"] = self.request.GET.get("next", "")
        return initial

    def form_valid(self, form):
        if self.request.user.is_anonymous:
            maybe_create_guest_user(self.request)
        return super().form_valid(form)


class CustomSignupView(HtmxAuthMixin, SignupView):
    htmx_template_name = "account/signup_content.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enable_guest_users"] = getattr(
            settings, "A4_ENABLE_GUEST_USERS", False
        )
        return context


class CustomLoginView(HtmxAuthMixin, LoginView):
    htmx_template_name = "account/login_content.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enable_guest_users"] = getattr(
            settings, "A4_ENABLE_GUEST_USERS", False
        )
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
