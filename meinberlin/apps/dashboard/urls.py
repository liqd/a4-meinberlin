from django.conf.urls import url

from meinberlin.apps.bplan.views import BplanProjectCreateView
from meinberlin.apps.dashboard2.urls import \
    urlpatterns as a4dashboard_urlpatterns
from meinberlin.apps.extprojects.views import ExternalProjectCreateView
from meinberlin.apps.projectcontainers.views import ContainerCreateView
from meinberlin.apps.projectcontainers.views import ContainerListView

from . import views

app_name = 'a4dashboard'

urlpatterns = [
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/settings/$',
        views.DashboardOrganisationUpdateView.as_view(),
        name='organisation-edit'),
    url(r'^newsletters/(?P<organisation_slug>[-\w_]+)/create/$',
        views.DashboardNewsletterCreateView.as_view(),
        name='newsletter-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/containers/$',
        ContainerListView.as_view(),
        name='container-list'),
    url(r'^projects/(?P<project_slug>[-\w_]+)/blueprints/$',
        views.ModuleBlueprintListView.as_view(),
        name='module-blueprint-list'),
    url(r'^projects/(?P<project_slug>[-\w_]+)/blueprints/'
        '(?P<blueprint_slug>[-\w_]+)/$',
        views.ModuleCreateView.as_view(),
        name='module-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/plans/$',
        views.PlanListView.as_view(),
        name='plan-list'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/plans/create/$',
        views.PlanCreateView.as_view(),
        name='plan-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)'
        r'/plans/(?P<slug>[-\w_]+)/$',
        views.PlanUpdateView.as_view(),
        name='plan-update'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)'
        r'/plans/(?P<slug>[-\w_]+)/delete/$',
        views.PlanDeleteView.as_view(),
        name='plan-delete'),

    # Overwrite adhocracy4 core urls with meinBerlin urls
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'external-project/$',
        ExternalProjectCreateView.as_view(),
        name='external-project-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'bplan/$',
        BplanProjectCreateView.as_view(),
        name='bplan-project-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/blueprints/'
        r'container/$',
        ContainerCreateView.as_view(),
        name='container-create'),
    url(r'^organisations/(?P<organisation_slug>[-\w_]+)/projects/$',
        views.DashboardProjectListView.as_view(),
        name='project-list'),
] + a4dashboard_urlpatterns
