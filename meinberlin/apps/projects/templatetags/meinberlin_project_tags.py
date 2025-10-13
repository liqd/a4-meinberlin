import itertools
import re

from django import template
from django.db.models import Q
from django.utils.html import strip_tags
from django.utils.translation import ngettext

from adhocracy4.comments.models import Comment
from adhocracy4.polls.models import Vote as Vote
from adhocracy4.ratings.models import Rating
from meinberlin.apps.budgeting.models import Proposal
from meinberlin.apps.dashboard import is_event_module
from meinberlin.apps.ideas.models import Idea
from meinberlin.apps.kiezkasse.models import Proposal as KKProposal
from meinberlin.apps.livequestions.models import LiveQuestion
from meinberlin.apps.mapideas.models import MapIdea

register = template.Library()


@register.filter
def project_url(project):
    if (
        project.project_type == "meinberlin_bplan.Bplan"
        or project.project_type == "meinberlin_extprojects.ExternalProject"
    ):
        return project.externalproject.url
    return project.get_absolute_url()


@register.filter
def is_external(project):
    return (
        project.project_type == "meinberlin_bplan.Bplan"
        or project.project_type == "meinberlin_extprojects.ExternalProject"
    )


@register.simple_tag(takes_context=True)
def get_sorted_modules(context):
    project = context["project"]
    module = context.get("module", None)
    module_qs = project.modules

    if module:
        module_qs = module.other_modules

    modules = list(
        itertools.chain(
            module_qs.running_modules(),
            module_qs.future_modules(),
            module_qs.past_modules(),
        )
    )
    # Remove offline modules from the module section in the project view
    return [m for m in modules if not is_event_module(m)]


@register.filter
def has_ckeditor_content(value):
    """
    Returns True if CKEditor field has meaningful content
    """
    if not value:
        return False

    # Strip HTML tags
    text = strip_tags(value)

    # Remove non-breaking spaces and whitespace
    text = re.sub(r"&nbsp;|\s", "", text)
    return len(text) > 0


@register.simple_tag(takes_context=True)
def get_offline_modules(context):
    project = context["project"]
    module_qs = project.modules
    modules = list(
        itertools.chain(
            module_qs.running_modules(),
            module_qs.future_modules(),
            module_qs.past_modules(),
        )
    )
    return [m for m in modules if is_event_module(m)]


@register.simple_tag
def get_first_item_event_type(module):
    """Return the event_type of the first OfflineEventItem of a module, if present."""
    from meinberlin.apps.offlineevents.models import OfflineEventItem

    first_item = module.item_set.first()
    if not first_item:
        return None

    try:
        offline_event_item = OfflineEventItem.objects.get(id=first_item.id)
        return offline_event_item.event_type
    except OfflineEventItem.DoesNotExist:
        return None


@register.inclusion_tag("meinberlin_projects/includes/module-tile/module_insights.html")
def render_module_insights(module):
    bp_type = module.blueprint_type
    count = 0
    label = ""
    icon = None

    type_to_model_mapping = {
        ("MIC", "MBS"): MapIdea,
        ("IC", "BS"): Idea,
        (
            "PB",
            "PB2",
            "PB3",
        ): Proposal,  # include PB3 for still existing modules
        ("KK",): KKProposal,  # include KK for still existing modules
        ("IE",): LiveQuestion,
    }

    rating_types = (
        "TP",
        "MTP",
    )
    comment_types = ("TR",)
    vote_types = ("PO",)

    for types, model in type_to_model_mapping.items():
        if bp_type in types:
            count = model.objects.filter(module=module).count()
            if model == Proposal or model == KKProposal:
                label = ngettext("Proposal", "Proposals", count)
                icon = "fas fa-pen"
            elif model == LiveQuestion:
                label = ngettext("Question", "Questions", count)
                icon = "fas fa-question"
            else:
                label = ngettext("Idea", "Ideas", count)
                icon = "far fa-lightbulb"

    if bp_type in rating_types:
        rating_values = [Rating.POSITIVE, Rating.NEGATIVE]
        count = Rating.objects.filter(
            Q(maptopic__module=module) | Q(topic__module=module),
            value__in=rating_values,
        ).count()
        label = ngettext("Rating", "Ratings", count)
        icon = "far fa-thumbs-up"

    if bp_type in comment_types:
        count = Comment.objects.filter(
            Q(paragraph__chapter__module=module)
            | Q(chapter__module=module)
            | Q(parent_comment__paragraph__chapter__module=module)
            | Q(parent_comment__chapter__module=module)
        ).count()
        label = ngettext("Comment", "Comments", count)
        icon = "far fa-comments"

    if bp_type in vote_types:
        count = (
            Vote.objects.filter(choice__question__poll__module=module)
            .values("creator")
            .distinct()
            .count()
        )
        label = ngettext("Participant", "Participants", count)
        icon = "fas fa-user-group"

    return {"count": count, "label": label, "icon": icon}
