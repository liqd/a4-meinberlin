import rules
from django.db.models import Q
from rules.predicates import is_superuser

from adhocracy4.comments.models import Comment

# content models used to detect contributions
from adhocracy4.modules.models import Item
from adhocracy4.organisations.predicates import is_initiator
from adhocracy4.polls.models import Answer
from adhocracy4.polls.models import Vote
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
    is_superuser
    | is_initiator
    | is_moderator
    | is_prj_group_member
    | ((is_public | is_project_member) & is_live),
)


@rules.predicate
def has_no_non_initiator_contributions(user, project):
    """True, if there are no contributions from non-initiators in the project."""
    initiator_ids = list(project.organisation.initiators.values_list("id", flat=True))

    # Wenn es keine Initiator:innen gibt, gelten alle Beiträge als Nicht‑Initiator‑Beiträge
    non_init_creator = ~Q(creator_id__in=initiator_ids) if initiator_ids else Q()

    has_items = (
        Item.objects.filter(module__project=project).filter(non_init_creator).exists()
    )
    has_comments = (
        Comment.objects.filter(project=project).filter(non_init_creator).exists()
    )
    has_votes = (
        Vote.objects.filter(choice__question__poll__module__project=project)
        .filter(non_init_creator)
        .exists()
    )
    has_answers = (
        Answer.objects.filter(question__poll__module__project=project)
        .filter(non_init_creator)
        .exists()
    )

    rating_q = (
        Q(idea__module__project=project)
        | Q(topic__module__project=project)
        | Q(mapidea__module__project=project)
        | Q(maptopic__module__project=project)
        | Q(budget_proposal__module__project=project)
        | Q(comment__project=project)
    )
    has_ratings = (
        Rating.objects.filter(rating_q)
        .filter(non_init_creator)
        .exclude(value=0)
        .exists()
    )

    return not (has_items or has_comments or has_votes or has_answers or has_ratings)


rules.set_perm(
    "a4projects.delete_project",
    is_superuser | (is_initiator & has_no_non_initiator_contributions),
)
