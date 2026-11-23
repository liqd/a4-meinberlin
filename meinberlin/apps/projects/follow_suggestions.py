from datetime import datetime
from datetime import timedelta
from datetime import timezone as datetime_timezone
from urllib.parse import urlencode

from django.urls import reverse
from django.utils import timezone

from adhocracy4.follows.models import Follow
from adhocracy4.projects.guest_users import is_guest_user

FOLLOW_SUGGESTION_INTERVAL = timedelta(days=30)

FOLLOW_SUGGESTION_TRIGGER_SESSION_KEY = "follow_suggestion_project"
FOLLOW_SUGGESTION_SHOWN_SESSION_KEY = "follow_suggestion_shown_at"
FOLLOW_SUGGESTION_CONFIRMATION_SESSION_KEY = "follow_suggestion_confirmed_project"


def is_guest(user):
    """Return True for anonymous visitors and temporary guest accounts."""
    return not user.is_authenticated or is_guest_user(user)


def is_regular_user(user):
    return user.is_authenticated and not is_guest_user(user)


def get_last_shown(request):
    """Return when the follow suggestion was last displayed for this request user."""
    if request.user.is_authenticated:
        return request.user.follow_suggestion_shown_at

    timestamp = request.session.get(FOLLOW_SUGGESTION_SHOWN_SESSION_KEY)
    if timestamp is None:
        return None

    try:
        return datetime.fromtimestamp(float(timestamp), tz=datetime_timezone.utc)
    except (TypeError, ValueError, OSError):
        return None


def may_show(request):
    last_shown = get_last_shown(request)
    return (
        last_shown is None or timezone.now() - last_shown >= FOLLOW_SUGGESTION_INTERVAL
    )


def mark_shown(request):
    """Remember that the suggestion was displayed.

    Logged-in users (including temporary guest accounts) store the timestamp on
    their account so the limit applies across browsers and devices. Anonymous
    visitors use the session.
    """
    now = timezone.now()
    if request.user.is_authenticated:
        request.user.follow_suggestion_shown_at = now
        request.user.save(update_fields=["follow_suggestion_shown_at"])
    else:
        request.session[FOLLOW_SUGGESTION_SHOWN_SESSION_KEY] = now.timestamp()


def is_following(user, project):
    return (
        is_regular_user(user)
        and Follow.objects.filter(project=project, creator=user, enabled=True).exists()
    )


def trigger(request, project):
    """Mark that the user has just performed an action in the project."""
    request.session[FOLLOW_SUGGESTION_TRIGGER_SESSION_KEY] = project.pk


def pop_trigger(request, project):
    """Return and clear the trigger if it belongs to the given project."""
    if request.session.get(FOLLOW_SUGGESTION_TRIGGER_SESSION_KEY) == project.pk:
        request.session.pop(FOLLOW_SUGGESTION_TRIGGER_SESSION_KEY, None)
        return True
    return False


def after_auth_url(request, project):
    """URL to return to after login/registration that also follows the project."""
    query = request.GET.copy()
    query["follow"] = project.slug
    return f"{request.path}?{query.urlencode()}"


def follow_after_auth_urls(request, project):
    next_url = after_auth_url(request, project)
    return {
        "signup_url": f"{reverse('account_signup')}?{urlencode({'next': next_url})}",
        "guest_convert_url": (
            f"{reverse('guest_convert')}?{urlencode({'next': next_url})}"
        ),
    }
