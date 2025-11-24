from django.urls import path

from . import api
from . import views

urlpatterns = [
    path("", views.AccountView.as_view(), name="account"),
    path("profile/", views.ProfileUpdateView.as_view(), name="account_profile"),
    path(
        "notification-settings/",
        views.NotificationSettingsView.as_view(),
        name="notification_settings",
    ),
    path("notifications/", views.NotificationsView.as_view(), name="notifications"),
    path("end-session/", api.EndSessionView.as_view(), name="end_session"),
    path(
        "followed-projects/",
        views.FollowedProjectsListView.as_view(),
        name="followed_projects",
    ),
]
