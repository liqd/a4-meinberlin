import rules

from adhocracy4.modules import predicates as module_predicates
from meinberlin.apps.contrib import predicates as contrib_predicates

rules.add_perm(
    'meinberlin_facetoface.view_facetoface',
    (module_predicates.is_project_admin |
     (module_predicates.is_allowed_view_item &
      contrib_predicates.has_context_started))
)
