from django.apps import apps
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

from adhocracy4.filters import views as filter_views
from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models

from . import filter
from . import forms
from . import get_project_dashboard
from . import mixins
from . import signals
from .blueprints import ProjectBlueprint
from .blueprints import get_blueprints

User = get_user_model()


def get_object_or_none(*args, **kwargs):
    try:
        return get_object_or_404(*args, **kwargs)
    except Http404:
        return None


class ProjectListView(mixins.DashboardBaseMixin,
                      mixins.DashboardProjectDuplicateMixin,
                      filter_views.FilteredListView):
    model = project_models.Project
    paginate_by = 12
    template_name = 'meinberlin_dashboard2/project_list.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'
    filter_set = filter.ProjectFilterSet

    def get_queryset(self):
        return super().get_queryset().filter(
            organisation=self.organisation
        )


class ContainerListView(mixins.DashboardBaseMixin,
                        mixins.DashboardProjectDuplicateMixin,
                        filter_views.FilteredListView):
    model = project_models.Project
    paginate_by = 12
    template_name = 'meinberlin_dashboard2/container_list.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'
    filter_set = filter.ProjectFilterSet

    def get_queryset(self):
        return super().get_queryset().filter(
            organisation=self.organisation
        )


class BlueprintListView(mixins.DashboardBaseMixin,
                        generic.TemplateView):
    template_name = 'meinberlin_dashboard2/blueprint_list.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'

    @property
    def blueprints(self):
        return get_blueprints()


class ProjectCreateView(mixins.DashboardBaseMixin,
                        mixins.BlueprintMixin,
                        generic.CreateView,
                        SuccessMessageMixin):
    model = project_models.Project
    slug_url_kwarg = 'project_slug'
    form_class = forms.ProjectCreateForm
    template_name = 'meinberlin_dashboard2/project_create_form.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'
    success_message = _('Project succesfully created.')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation'] = self.organisation
        kwargs['creator'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('a4dashboard:project-edit',
                       kwargs={'project_slug': self.object.slug})

    def form_valid(self, form):
        response = super().form_valid(form)
        self._create_modules_and_phases(self.object)

        return response

    def _create_modules_and_phases(self, project):
        module = module_models.Module(
            name='Onlinebeteiligung',
            description=project.description,
            weight=1,
            project=project,
        )
        module.save()

        self._create_module_settings(module)
        self._create_phases(module, self.blueprint.content)

    def _create_module_settings(self, module):
        if self.blueprint.settings_model:
            settings_model = apps.get_model(*self.blueprint.settings_model)
            module_settings = settings_model(module=module)
            module_settings.save()

    def _create_phases(self, module, blueprint_phases):
        for phase_content in blueprint_phases:
            phase = phase_models.Phase(
                type=phase_content.identifier,
                name=phase_content.name,
                description=phase_content.description,
                weight=phase_content.weight,
                module=module,
            )
            phase.save()


class ContainerCreateView(ProjectCreateView):
    blueprint = ProjectBlueprint(
        title=_('Container'),
        description=_(
            'A container contains multiple projects.'
        ),
        content=[],
        image='images/container.svg',
        settings_model=None,
    )


class ProjectUpdateView(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        project = get_object_or_404(project_models.Project,
                                    slug=kwargs['project_slug'])
        dashboard = get_project_dashboard(project)
        component = dashboard.get_project_components()[0]
        return component.get_base_url(project)


class ProjectPublishView(mixins.DashboardBaseMixin,
                         SingleObjectMixin,
                         generic.View):
    permission_required = 'a4projects.add_project'
    model = project_models.Project
    slug_url_kwarg = 'project_slug'

    def post(self, request, *args, **kwargs):
        self.project = self.get_object()

        action = request.POST.get('action', None)
        if action == 'publish':
            self.publish_project()
        elif action == 'unpublish':
            self.unpublish_project()
        else:
            messages.warning(self.request, _('Invalid action'))

        return HttpResponseRedirect(self.get_next())

    def get_next(self):
        if 'referrer' in self.request.POST:
            return self.request.POST['referrer']
        elif 'HTTP_REFERER' in self.request.META:
            return self.request.META['HTTP_REFERER']

        return reverse('a4dashboard:project-edit', kwargs={
            'project_slug': self.project.slug
        })

    def publish_project(self):
        if not self.project.is_draft:
            messages.info(self.request, _('Project is already published'))
            return

        dashboard = get_project_dashboard(self.project)

        num_valid, num_required = dashboard.get_progress()
        is_complete = (num_valid == num_required)

        if not is_complete:
            messages.error(self.request,
                           _('Project cannot be published. '
                             'Required fields are missing.'))
            return

        responses = signals.project_pre_publish.send(sender=None,
                                                     project=self.project)
        errors = [str(msg) for func, msg in responses if msg]
        if errors:
            msg = _('Project cannot be published.') + ' \n' + '\n'.join(errors)
            messages.error(self.request, msg)
            return

        self.project.is_draft = False
        self.project.save()
        signals.project_published.send(sender=None, project=self.project)

        messages.success(self.request,
                         _('Project successfully published.'))

    def unpublish_project(self):
        if self.project.is_draft:
            messages.info(self.request, _('Project is already unpublished'))
            return

        self.project.is_draft = True
        self.project.save()
        signals.project_unpublished.send(sender=None, project=self.project)
        messages.success(self.request,
                         _('Project successfully unpublished.'))
