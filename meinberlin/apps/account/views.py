from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic.base import RedirectView
from rest_framework.renderers import JSONRenderer
from rules.contrib.views import LoginRequiredMixin

from adhocracy4.actions.models import Action
from meinberlin.apps.notifications.serializers import NotificationSettingsSerializer
from meinberlin.apps.users.models import User

from . import forms


class AccountView(RedirectView):
    permanent = False
    pattern_name = "account_profile"
    # Placeholder View to be replaced if we want to use a custom account
    # dashboard function overview.


class ProfileUpdateView(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):

    model = User
    template_name = "meinberlin_account/profile.html"
    form_class = forms.ProfileForm
    success_message = _("Your profile was successfully updated.")

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_success_url(self):
        return self.request.path


class ProfileActionsView(LoginRequiredMixin, generic.ListView):

    model = Action
    paginate_by = 10
    template_name = "meinberlin_account/actions.html"

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.request.user.id)
        qs = super().get_queryset()
        qs = qs.filter(project__follow__creator=user, project__follow__enabled=True)
        return qs.exclude_updates()


class NotificationsView(LoginRequiredMixin, generic.TemplateView):
    template_name = "meinberlin_account/notifications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["show_restricted"] = (
            user.project_moderator.exists() or len(user.organisations) > 0
        )

        data = NotificationSettingsSerializer(user.notification_settings).data
        context["data"] = JSONRenderer().render(data).decode("utf-8")
        context["api_url"] = reverse(
            "notification-settings-detail",
            kwargs={"pk": user.notification_settings.id},
        )
        return context
