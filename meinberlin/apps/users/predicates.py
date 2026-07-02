import rules

from adhocracy4.modules.predicates import is_owner
from adhocracy4.projects.guest_users import is_guest_user


@rules.predicate
def is_authenticated_and_owner(user, item):
    return rules.is_authenticated(user) & is_owner(user, item)


@rules.predicate
def is_regular_user(user):
    """A logged-in, non-guest user.

    ``is_guest_user`` safely returns ``False`` when django-guest-user is not
    installed, so this predicate degrades to ``is_authenticated``.
    """
    return bool(user.is_authenticated) and not is_guest_user(user)


@rules.predicate
def is_regular_user_and_owner(user, item):
    return is_regular_user(user) & is_owner(user, item)
