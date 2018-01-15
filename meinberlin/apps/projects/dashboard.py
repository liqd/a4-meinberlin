from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.dashboard2 import DashboardComponent
from meinberlin.apps.dashboard2 import ProjectFormComponent
from meinberlin.apps.dashboard2 import components

from . import forms
from . import views


class ParticipantsComponent(DashboardComponent):
    identifier = 'participants'
    weight = 30
    label = _('Participants')

    def is_effective(self, project):
        return not project.is_draft and project.is_private

    def get_base_url(self, project):
        return reverse('a4dashboard:dashboard-participants-edit', kwargs={
            'project_slug': project.slug
        })

    def get_urls(self):
        return [(
            r'^projects/(?P<project_slug>[-\w_]+)/participants/$',
            views.DashboardProjectParticipantsView.as_view(component=self),
            'dashboard-participants-edit'
        )]


class ModeratorsComponent(DashboardComponent):
    identifier = 'moderators'
    weight = 32
    label = _('Moderators')

    def is_effective(self, project):
        return True

    def get_base_url(self, project):
        return reverse('a4dashboard:dashboard-moderators-edit', kwargs={
            'project_slug': project.slug
        })

    def get_urls(self):
        return [(
            r'^projects/(?P<project_slug>[-\w_]+)/moderators/$',
            views.DashboardProjectModeratorsView.as_view(component=self),
            'dashboard-moderators-edit'
        )]


class ProjectInformationSectionsComponent(ProjectFormComponent):
    identifier = 'project-information-sections'
    weight = 11  # should be 12 actually
    label = _('Extended Information')

    form_title = _('Extended Project Information')
    form_class = forms.ProjectInformationSectionFormSet
    form_template_name = 'meinberlin_projects/includes' \
                         '/project_information_sections_form.html'

    def get_progress(self, object):
        return 0, 0


components.register_project(ModeratorsComponent())
components.register_project(ParticipantsComponent())
components.register_project(ProjectInformationSectionsComponent())
