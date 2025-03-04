import factory
import pytest
from django.utils.translation import ngettext

from adhocracy4.polls import phases as voting_phases
from adhocracy4.test.helpers import render_template
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases as budgeting_phases
from meinberlin.apps.documents import phases as textreview_phases
from meinberlin.apps.ideas import phases as idea_phases
from meinberlin.apps.livequestions import phases as livequestion_phases
from meinberlin.apps.projects.templatetags.meinberlin_project_tags import (
    render_module_insights,
)
from meinberlin.apps.topicprio import phases as topicprio_phases
from tests.helpers import clear_query_cache


@pytest.mark.django_db
def test_project_url(project, external_project_factory, bplan_factory):
    external_project = external_project_factory(url=factory.Faker("url"))
    bplan = bplan_factory(url=factory.Faker("url"))
    template = "{% load meinberlin_project_tags %}" "{{ project|project_url }}"

    assert project.get_absolute_url() == render_template(template, {"project": project})
    assert external_project.externalproject.url == render_template(
        template, {"project": external_project}
    )
    assert bplan.externalproject.url == render_template(template, {"project": bplan})


@pytest.mark.django_db
def test_is_external(project, external_project, bplan):
    template = (
        "{% load meinberlin_project_tags %}"
        "{% if project|is_external %}"
        "is external"
        "{% else %}"
        "is not external"
        "{% endif %}"
    )

    assert "is not external" == render_template(template, {"project": project})
    assert "is external" == render_template(template, {"project": external_project})
    assert "is external" == render_template(template, {"project": bplan})


@pytest.mark.django_db
def test_is_a4_project(project, external_project, bplan):
    template = (
        "{% load meinberlin_project_tags %}"
        '{% if project.project_type == "a4projects.Project" %}'
        "is a4 project"
        "{% else %}"
        "is no a4 project"
        "{% endif %}"
    )

    assert "is a4 project" == render_template(template, {"project": project})
    assert "is no a4 project" == render_template(
        template, {"project": external_project}
    )
    assert "is no a4 project" == render_template(template, {"project": bplan})


@pytest.mark.django_db
def test_render_module_insights(
    django_assert_num_queries,
    module_factory,
    phase_factory,
    idea_factory,
    proposal_factory,
    comment_factory,
    live_question_factory,
    topic_factory,
    rating_factory,
    chapter_factory,
    poll_factory,
    question_factory,
    choice_factory,
    vote_factory,
):
    phase_ic, module_ic, project_ic, idea = setup_phase(
        phase_factory,
        idea_factory,
        idea_phases.FeedbackPhase,
        module__blueprint_type="IC",
    )

    phase_pb, module_pb, project_pb, proposal = setup_phase(
        phase_factory,
        proposal_factory,
        budgeting_phases.CollectPhase,
        module__blueprint_type="PB",
    )

    phase_ie, module_ie, project_ie, question = setup_phase(
        phase_factory,
        live_question_factory,
        livequestion_phases.IssuePhase,
        module__blueprint_type="IE",
    )

    phase_tp, module_tp, project_tp, topic = setup_phase(
        phase_factory,
        topic_factory,
        topicprio_phases.PrioritizePhase,
        module__blueprint_type="TP",
    )

    phase_tr, module_tr, project_tr, chapter = setup_phase(
        phase_factory,
        chapter_factory,
        textreview_phases.CommentPhase,
        module__blueprint_type="TR",
    )

    phase_po, module_po, project_po, poll = setup_phase(
        phase_factory,
        poll_factory,
        voting_phases.VotingPhase,
        module__blueprint_type="PO",
    )

    # test the default case with no items
    empty_module = module_factory()

    clear_query_cache()
    with django_assert_num_queries(0):
        data = render_module_insights(empty_module)
        assert data["count"] == 0
        assert data["label"] == ""
        assert data["icon"] is None

    # idea module
    clear_query_cache()
    with django_assert_num_queries(1):
        data = render_module_insights(module_ic)
        assert data["count"] == 1
        assert data["label"] == ngettext("Idea", "Ideas", 1)
        assert data["icon"] == "far fa-lightbulb"

    # budgeting
    proposal_factory(module=module_pb)
    clear_query_cache()
    with django_assert_num_queries(1):
        data = render_module_insights(module_pb)
        assert data["count"] == 2
        assert data["label"] == ngettext("Proposal", "Proposals", 2)
        assert data["icon"] == "fas fa-pen"

    # Live Questions
    live_question_factory(module=module_ie)
    live_question_factory(module=module_ie)
    clear_query_cache()
    with django_assert_num_queries(1):
        data = render_module_insights(module_ie)
        assert data["count"] == 3
        assert data["label"] == ngettext("Question", "Questions", 3)
        assert data["icon"] == "fas fa-question"

    # topic prio - count ratings
    clear_query_cache()
    rating_factory(content_object=topic)
    rating_factory(content_object=topic)
    with django_assert_num_queries(2):
        data = render_module_insights(module_tp)
        assert data["count"] == 2
        assert data["label"] == ngettext("Rating", "Ratings", 2)
        assert data["icon"] == "far fa-thumbs-up"

    # textreview - count comments
    comment = comment_factory(content_object=chapter)
    comment_factory(content_object=comment)
    clear_query_cache()
    with django_assert_num_queries(4):
        data = render_module_insights(module_tr)
        assert data["count"] == 2
        assert data["label"] == ngettext("Comment", "Comments", 2)
        assert data["icon"] == "far fa-comments"

    # polls - count participants
    question = question_factory(poll=poll)
    choice1 = choice_factory(question=question)

    vote_factory(choice=choice1)
    vote_factory(choice=choice1)
    vote_factory(choice=choice1)
    clear_query_cache()
    with django_assert_num_queries(1):
        data = render_module_insights(module_po)
        assert data["count"] == 3
        assert data["label"] == ngettext("Participant", "Participants", 3)
        assert data["icon"] == "fas fa-user-group"
