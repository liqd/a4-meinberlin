from django.shortcuts import redirect

from adhocracy4.follows.models import Follow
from adhocracy4.projects.models import Project

from . import follow_suggestions


class FollowSuggestionMiddleware:
    """Handle the follow marker used by the guest follow suggestion.

    Guest visitors are sent to registration/login with ``?follow=<project>`` in
    the return URL. Once they are a regular user, the project is followed and
    the confirmation banner is shown on the returned page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.follow_suggestion_confirmed_project = None

        follow_slug = request.GET.get("follow")
        if (
            request.method == "GET"
            and follow_slug
            and follow_suggestions.is_regular_user(request.user)
        ):
            project = Project.objects.filter(slug=follow_slug).first()
            if project:
                Follow.objects.update_or_create(
                    project=project,
                    creator=request.user,
                    defaults={"enabled": True},
                )
                request.session[
                    follow_suggestions.FOLLOW_SUGGESTION_CONFIRMATION_SESSION_KEY
                ] = project.pk

                query = request.GET.copy()
                query.pop("follow", None)
                url = request.path
                if query:
                    url = f"{url}?{query.urlencode()}"
                return redirect(url)

        if request.user.is_authenticated:
            request.follow_suggestion_confirmed_project = request.session.pop(
                follow_suggestions.FOLLOW_SUGGESTION_CONFIRMATION_SESSION_KEY,
                None,
            )
        else:
            request.session.pop(
                follow_suggestions.FOLLOW_SUGGESTION_CONFIRMATION_SESSION_KEY, None
            )

        return self.get_response(request)
