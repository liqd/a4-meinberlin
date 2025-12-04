from datetime import timedelta

import pytest
from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.core.management import call_command

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs
from adhocracy4.dashboard import signals
from adhocracy4.phases.models import Phase
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases

START = Verbs.START.value


@pytest.mark.django_db
def test_phase_started_email(apiclient, phase_factory, proposal_factory):
    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    phase.end_date += timedelta(hours=48)
    phase.save()
    phase.refresh_from_db()

    content_type = ContentType.objects.get_for_model(Phase)
    action_count = Action.objects.filter(
        verb=START, obj_content_type=content_type
    ).count()
    assert action_count == 0

    with freeze_phase(phase):
        call_command("create_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        assert action_count == 1
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject.startswith("Los geht's:")


@pytest.mark.django_db
def test_phase_started_draft_no_email(apiclient, phase_factory, proposal_factory):
    phase, module, project, proposal = setup_phase(
        phase_factory, proposal_factory, phases.VotingPhase
    )
    project = phase.module.project
    project.is_draft = True
    project.save()
    project.refresh_from_db()

    phase.end_date += timedelta(hours=48)
    phase.save()
    phase.refresh_from_db()

    content_type = ContentType.objects.get_for_model(Phase)
    action_count = Action.objects.filter(
        verb=START, obj_content_type=content_type
    ).count()
    assert action_count == 0

    with freeze_phase(phase):
        call_command("create_system_actions")
        action_count = Action.objects.filter(
            verb=START, obj_content_type=content_type
        ).count()
        assert action_count == 0
        assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_search_profile_matches(search_factories, phase_factory, user):
    phase, module, project, _ = setup_phase(
        phase_factory, None, phases.CollectPhase, module__project__name="Berlin"
    )
    project = phase.module.project

    matching_profile, non_matching_profile_same_user, matching_profile_other_user = (
        search_factories
    )
    signals.project_published.send(sender=None, project=project, user=user)

    assert len(mail.outbox) == 2
    recipients = mail.outbox[0].recipients() + mail.outbox[1].recipients()
    assert mail.outbox[0].subject.startswith(
        "Neues Projekt entsprechend Ihrer Gespeicherten Suche:"
    )
    assert matching_profile.creator.email in recipients
    assert matching_profile_other_user.creator.email in recipients
