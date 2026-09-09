import rules
from django.db.models import Q
from rules.predicates import is_superuser

from adhocracy4.comments.models import Comment

# content models used to detect contributions
from adhocracy4.modules.models import Item
from adhocracy4.organisations.predicates import is_initiator
from adhocracy4.polls.models import Answer
from adhocracy4.polls.models import Vote
from adhocracy4.projects.predicates import guest_may_participate
from adhocracy4.projects.predicates import is_live
from adhocracy4.projects.predicates import is_moderator
from adhocracy4.projects.predicates import is_prj_group_member
from adhocracy4.projects.predicates import is_project_member
from adhocracy4.projects.predicates import is_public
from adhocracy4.projects.predicates import is_semipublic
from adhocracy4.ratings.models import Rating

rules.remove_perm("a4projects.view_project")
rules.add_perm(
    "a4projects.view_project",
    is_superuser
    | is_initiator
    | is_moderator
    | is_prj_group_member
    | ((is_public | is_semipublic | is_project_member) & is_live),
)

rules.set_perm(
    "a4projects.participate_in_project",
    is_superuser | is_initiator | is_moderator | is_prj_group_member
    # guest_may_participate is True for non-guests and evaluates to
    # project.allow_guest_users for guest users, so the AND only gates guests.
    | ((is_public | is_project_member) & is_live & guest_may_participate),
)


@rules.predicate
def has_no_participant_contributions(user, project):
    """True, if there are no contributions from participants in the project."""
    safe_creator_ids = set(project.organisation.initiators.values_list("id", flat=True))
    if project.group_id and (
        is_initiator(user, project) or is_prj_group_member(user, project)
    ):
        safe_creator_ids.update(project.group.user_set.values_list("id", flat=True))

    participant_creator = ~Q(creator_id__in=safe_creator_ids)

    rating_q = (
        Q(idea__module__project=project)
        | Q(topic__module__project=project)
        | Q(mapidea__module__project=project)
        | Q(maptopic__module__project=project)
        | Q(budget_proposal__module__project=project)
        | Q(comment__project=project)
    )
    contributions = (
        Item.objects.filter(module__project=project),
        Comment.objects.filter(project=project),
        Vote.objects.filter(choice__question__poll__module__project=project),
        Answer.objects.filter(question__poll__module__project=project),
        Rating.objects.filter(rating_q).exclude(value=0),
    )

    return not any(qs.filter(participant_creator).exists() for qs in contributions)


rules.set_perm(
    "a4projects.delete_project",
    is_superuser
    | ((is_initiator | is_prj_group_member) & has_no_participant_contributions),
)
