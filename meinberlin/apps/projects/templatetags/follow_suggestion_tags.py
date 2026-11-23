from django import template
from django.urls import reverse

from .. import follow_suggestions

register = template.Library()


@register.inclusion_tag(
    "meinberlin_projects/includes/follow_suggestion.html", takes_context=True
)
def follow_suggestion(context, project):
    request = context.get("request")
    if not request or not project:
        return {"render": False}

    confirmed_project = getattr(request, "follow_suggestion_confirmed_project", None)
    confirmation_auth = confirmed_project == project.pk

    if confirmation_auth:
        initial_trigger = False
    else:
        initial_trigger = follow_suggestions.pop_trigger(request, project)

        if follow_suggestions.is_following(request.user, project):
            return {"render": False}

        if not follow_suggestions.may_show(request):
            return {"render": False}

    guest = follow_suggestions.is_guest(request.user)
    auth_urls = follow_suggestions.follow_after_auth_urls(request, project)

    return {
        "render": True,
        "project": project,
        "guest": guest,
        "confirmation_auth": confirmation_auth,
        "initial_trigger": initial_trigger,
        "claim_url": reverse("follow_suggestion_claim", kwargs={"slug": project.slug}),
        "follow_url": reverse("follows-detail", kwargs={"project__slug": project.slug}),
        "notification_settings_url": reverse("notification_settings"),
        "followed_projects_url": reverse("followed_projects"),
        **auth_urls,
    }
