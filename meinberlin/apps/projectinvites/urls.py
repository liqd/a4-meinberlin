from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^participant/(?P<invite_token>[-\w_]+)/$',
        views.ParticipantInviteDetailView.as_view(),
        name='project-participant-invite-detail'),
    url(r'^participant/(?P<invite_token>[-\w_]+)/accept/$',
        views.ParticipantInviteUpdateView.as_view(),
        name='project-participant-invite-update'),
    url(r'^moderator/(?P<invite_token>[-\w_]+)/$',
        views.ModeratorInviteDetailView.as_view(),
        name='project-moderator-invite-detail'),
    url(r'^moderator/(?P<invite_token>[-\w_]+)/accept/$',
        views.ModeratorInviteUpdateView.as_view(),
        name='project-moderator-invite-update'),
]
