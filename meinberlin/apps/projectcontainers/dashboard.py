from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.dashboard import get_project_type
from meinberlin.apps.dashboard2 import ProjectFormComponent
from meinberlin.apps.dashboard2 import components

from . import forms
from . import views


class ContainerProjectComponent(ProjectFormComponent):
    identifier = 'container-basic'
    weight = 10
    label = _('Basic settings')

    form_title = _('Edit container settings')
    form_class = forms.ContainerProjectForm
    form_template_name = 'meinberlin_projectcontainers/includes' \
                         '/container_project_basic_form.html'

    def is_effective(self, project):
        project_type = get_project_type(project)
        return project_type == 'container'

    def get_base_url(self, project):
        return reverse('a4dashboard:dashboard-container-basic-edit', kwargs={
            'project_slug': project.slug
        })

    def get_urls(self):
        return [(
            r'^projects/(?P<project_slug>[-\w_]+)/container/$',
            views.ContainerProjectUpdateView.as_view(
                component=self,
                title=self.form_title,
                form_class=self.form_class,
                form_template_name=self.form_template_name
            ),
            'dashboard-container-basic-edit'
        )]


class ContainerProjectsComponent(ProjectFormComponent):
    identifier = 'container-projects'
    weight = 20
    label = _('Projects')

    form_title = _('Select projects')
    form_class = forms.ContainerProjectsForm
    form_template_name = 'meinberlin_projectcontainers/includes' \
                         '/container_projects_form.html'

    def is_effective(self, project):
        project_type = get_project_type(project)
        return project_type == 'container'

    def get_base_url(self, project):
        return reverse('a4dashboard:dashboard-container-projects', kwargs={
            'project_slug': project.slug
        })

    def get_urls(self):
        return [(
            r'^projects/(?P<project_slug>[-\w_]+)/container-projects/$',
            views.ContainerProjectsView.as_view(
                component=self,
                title=self.form_title,
                form_class=self.form_class,
                form_template_name=self.form_template_name
            ),
            'dashboard-container-projects'
        )]

    def get_progress(self, project):
        return (1, 1)


components.register_project(ContainerProjectComponent())
components.register_project(ContainerProjectsComponent())
