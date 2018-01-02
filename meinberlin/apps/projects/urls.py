from django.conf.urls import url

from adhocracy4.projects.urls import urlpatterns as a4_projects_urls
from meinberlin.apps.projectinvites import views as projectinviteviews

from . import views

urlpatterns = [
    url(r'^$', views.ProjectListView.as_view(),
        name='project-list'),

    # Legacy links for old invites sent by email
    url(r'^participant-invites/(?P<invite_token>[-\w_]+)/$',
        projectinviteviews.ParticipantInviteDetailRedirectView.as_view()),
    url(r'^moderator-invites/(?P<invite_token>[-\w_]+)/$',
        projectinviteviews.ModeratorInviteDetailRedirectView.as_view()),
]

urlpatterns += a4_projects_urls
