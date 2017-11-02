import rules
from rules.predicates import is_superuser

from adhocracy4.organisations.predicates import is_initiator

rules.add_perm(
    'meinberlin_plans.list_plan',
    rules.always_allow
)

rules.add_perm(
    'meinberlin_plans.view_plan',
    rules.always_allow
)

rules.add_perm(
    'meinberlin_plans.add_plan',
    is_superuser | is_initiator
)

rules.add_perm(
    'meinberlin_plans.change_plan',
    is_superuser | is_initiator
)
