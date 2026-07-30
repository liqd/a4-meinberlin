from urllib.parse import urlparse

from allauth.account.views import LoginView
from allauth.account.views import SignupView
from django.conf import settings
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import FormView
from guest_user.functions import maybe_create_guest_user

from .forms import GuestCreateForm


class GuestCreateView(FormView):
    """Terms + captcha gate; on submit start a guest session and redirect back."""

    form_class = GuestCreateForm
    template_name = "meinberlin_users/guest_create.html"

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


class CustomSignupView(SignupView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enable_guest_users"] = getattr(
            settings, "A4_ENABLE_GUEST_USERS", False
        )
        return context


class CustomLoginView(LoginView):
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
