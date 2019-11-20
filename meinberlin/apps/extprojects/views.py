from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.dashboard.blueprints import ProjectBlueprint
from adhocracy4.dashboard.components.forms.views import \
    ProjectComponentFormView
from adhocracy4.dashboard.mixins import DashboardBaseMixin
from adhocracy4.dashboard.views import ProjectCreateView
from meinberlin.apps.extprojects import phases as extprojects_phases

from . import apps
from . import forms
from . import models


class ExternalProjectCreateView(ProjectCreateView):

    model = models.ExternalProject
    slug_url_kwarg = 'project_slug'
    form_class = forms.ExternalProjectCreateForm
    template_name = 'meinberlin_extprojects/external_project_create_form.html'
    success_message = _('External project successfully created.')

    blueprint = ProjectBlueprint(
        title=_('Linkage'),
        description=_(
            'Linkages are handled on a different platform.'
        ),
        content=[
            extprojects_phases.ExternalPhase(),
        ],
        image='',
        settings_model=None,
    )


class ExternalProjectUpdateView(ProjectComponentFormView):

    model = models.ExternalProject

    @property
    def project(self):
        project = super().project
        return project.externalproject

    def get_object(self, queryset=None):
        return self.project


class ExternalProjectListView(DashboardBaseMixin,
                              generic.ListView):
    model = models.ExternalProject
    paginate_by = 12
    template_name = 'meinberlin_extprojects/dashboard_extproject_list.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    def get_queryset(self):
        project_type = '{}.{}'.format(
            apps.Config.label,
            'ExternalProject'
        )
        return super().get_queryset().filter(
            organisation=self.organisation,
            project_type=project_type
        )

    def get_permission_object(self):
        return self.organisation
