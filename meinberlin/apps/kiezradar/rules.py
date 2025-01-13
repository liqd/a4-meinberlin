import rules

from meinberlin.apps.users.predicates import is_authenticated_and_owner

# we only require is_authenticated here as the serializer filters the queryset by user
rules.add_perm("meinberlin_kiezradar.view_kiezradar", rules.is_authenticated)

rules.add_perm("meinberlin_kiezradar.add_kiezradar", rules.is_authenticated)

rules.add_perm("meinberlin_kiezradar.change_kiezradar", is_authenticated_and_owner)

rules.add_perm("meinberlin_kiezradar.delete_kiezradar", is_authenticated_and_owner)


# we only require is_authenticated here as the serializer filters the queryset by user
rules.add_perm("meinberlin_kiezradar.view_searchprofile", rules.is_authenticated)

rules.add_perm("meinberlin_kiezradar.add_searchprofile", rules.is_authenticated)

rules.add_perm("meinberlin_kiezradar.change_searchprofile", is_authenticated_and_owner)

rules.add_perm("meinberlin_kiezradar.delete_searchprofile", is_authenticated_and_owner)
