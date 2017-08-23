from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from . import DashboardComponent
from . import ModuleFormComponent
from . import ModuleFormSetComponent
from . import ProjectFormComponent
from . import content
from . import forms
from . import views


class ProjectBasicComponent(ProjectFormComponent):
    identifier = 'basic'
    weight = 10

    menu_label = _('Basic settings')
    form_title = _('Edit basic settings')
    form_class = forms.ProjectBasicForm
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/project_basic_form.html'


class ProjectInformationComponent(ProjectFormComponent):
    identifier = 'information'
    weight = 11

    menu_label = _('Information')
    form_title = _('Edit project information')
    form_class = forms.ProjectInformationForm
    form_template_name = 'meinberlin_dashboard2' \
                         '/includes/project_information_form.html'


class ModuleBasicComponent(ModuleFormComponent):
    identifier = 'module_basic'
    weight = 10

    menu_label = _('Basic information')
    form_title = _('Edit basic module information')
    form_class = forms.ModuleBasicForm
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/module_basic_form.html'


class ModulePhasesComponent(ModuleFormSetComponent):
    identifier = 'phases'
    weight = 11

    menu_label = _('Phases')
    form_title = _('Edit phases information')
    form_class = forms.PhaseFormSet
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/module_phases_form.html'


class ParticipantsComponent(DashboardComponent):
    identifier = 'participants'
    weight = 30

    def get_menu_label(self, project):
        if project.is_private:
            return _('Participants')
        return ''

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
    weight = 31

    def get_menu_label(self, project):
        return _('Moderators')

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


content.register_project(ProjectBasicComponent())
content.register_project(ProjectInformationComponent())
content.register_project(ModeratorsComponent())
content.register_project(ParticipantsComponent())
content.register_module(ModuleBasicComponent())
content.register_module(ModulePhasesComponent())
