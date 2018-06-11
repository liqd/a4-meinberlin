from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.generic.base import RedirectView
from rules.contrib.views import LoginRequiredMixin

from adhocracy4.actions.models import Action
from meinberlin.apps.users.models import User

from . import forms


class AccountView(RedirectView):
    permanent = False
    pattern_name = 'account_profile'
    # Placeholder View to be replaced if we want to use a custom account
    # dashboard function overview.


class ProfileUpdateView(SuccessMessageMixin,
                        LoginRequiredMixin,
                        generic.UpdateView):

    model = User
    template_name = 'meinberlin_account/profile.html'
    form_class = forms.ProfileForm
    success_message = _('Your profile was successfully updated.')

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_success_url(self):
        return self.request.path


class BaseActivityView(LoginRequiredMixin,
                       generic.ListView):

    model = Action
    paginate_by = 10
    template_name = 'meinberlin_account/actions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['hint'] = self.hint
        return context


class ProfileActionsView(BaseActivityView):

    title = _('Activities')
    hint = _(
        'Here you can find any actions that have happened in projects you are'
        ' following.')

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.request.user.id)
        qs = super().get_queryset()
        qs = qs.filter(project__follow__creator=user,
                       project__follow__enabled=True)
        return qs.exclude_updates()


class ProfileUserActionsView(BaseActivityView):

    title = _('My Activities')
    hint = _('Here you can see your contributions.')

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.request.user.id)
        qs = super().get_queryset()
        qs = qs.filter(actor=user)
        return qs.exclude_updates()
