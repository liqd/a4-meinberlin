from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils import functional
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.projects import models as project_models
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.dashboard import forms as old_forms
from meinberlin.apps.newsletters.forms import NewsletterForm
from meinberlin.apps.newsletters.views import NewsletterCreateView
from meinberlin.apps.organisations.models import Organisation

User = get_user_model()


class DashboardBaseMixin:

    @functional.cached_property
    def organisation(self):
        if 'organisation_slug' in self.kwargs:
            slug = self.kwargs['organisation_slug']
            return get_object_or_404(Organisation, slug=slug)

    def get_permission_object(self):
        return self.organisation


class DashboardProjectListView(DashboardBaseMixin,
                               rules_mixins.PermissionRequiredMixin,
                               generic.ListView):
    model = project_models.Project
    paginate_by = 12
    template_name = 'meinberlin_dashboard2/project_list.html'
    permission_required = 'a4projects.add_project'

    def get_queryset(self):
        return super().get_queryset().filter(
            organisation=self.organisation
        )


class DashboardOrganisationUpdateView(DashboardBaseMixin,
                                      rules_mixins.PermissionRequiredMixin,
                                      SuccessMessageMixin,
                                      generic.UpdateView):

    model = Organisation
    form_class = old_forms.OrganisationForm
    slug_url_kwarg = 'organisation_slug'
    template_name = 'meinberlin_dashboard2/organisation_form.html'
    success_message = _('Organisation successfully updated.')
    permission_required = 'meinberlin_organisations.change_organisation'
    menu_item = 'organisation'


class DashboardNewsletterCreateView(DashboardBaseMixin,
                                    NewsletterCreateView):
    template_name = 'meinberlin_dashboard2/newsletter_form.html'
    menu_item = 'newsletter'
    form_class = NewsletterForm
    permission_required = 'a4projects.add_project'

    def get_email_kwargs(self):
        kwargs = {}
        kwargs.update({'organisation_pk': self.organisation.pk})
        return kwargs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation'] = self.organisation
        kwargs.pop('user')
        return kwargs

    def get_success_url(self):
        return reverse(
            'dashboard2-newsletter-create',
            kwargs={'organisation_slug': self.organisation.slug})
