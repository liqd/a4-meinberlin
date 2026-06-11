import rules

from adhocracy4.organisations.predicates import is_initiator

# The rules add_bplan and change_bplan are only used when bplans are created
# or updated via the API. Here group-members cannot do that,
# while via the dashboard they can.

rules.add_perm("meinberlin_bplan.add_bplan", is_initiator)

rules.add_perm("meinberlin_bplan.change_bplan", is_initiator)
