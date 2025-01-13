import rules

from adhocracy4.modules.predicates import is_owner


@rules.predicate
def is_authenticated_and_owner(user, item):
    return rules.is_authenticated(user) & is_owner(user, item)
