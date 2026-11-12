import rules

from meinberlin.apps.users.predicates import is_regular_user
from meinberlin.apps.users.predicates import is_regular_user_and_owner

# guests are excluded: saved searches/radars belong to permanent accounts only.
# we only require regular-user here as the serializer filters the queryset by user
rules.add_perm("meinberlin_kiezradar.view_kiezradar", is_regular_user)

rules.add_perm("meinberlin_kiezradar.add_kiezradar", is_regular_user)

rules.add_perm("meinberlin_kiezradar.change_kiezradar", is_regular_user_and_owner)

rules.add_perm("meinberlin_kiezradar.delete_kiezradar", is_regular_user_and_owner)


# we only require regular-user here as the serializer filters the queryset by user
rules.add_perm("meinberlin_kiezradar.view_searchprofile", is_regular_user)

rules.add_perm("meinberlin_kiezradar.add_searchprofile", is_regular_user)

rules.add_perm("meinberlin_kiezradar.change_searchprofile", is_regular_user_and_owner)

rules.add_perm("meinberlin_kiezradar.delete_searchprofile", is_regular_user_and_owner)
