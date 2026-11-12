from datetime import timedelta

import pytest
from django.core import mail
from django.test.utils import override_settings
from django.utils import timezone

from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.adminlog.models import PROJECT_COMPONENT_UPDATED
from meinberlin.apps.adminlog.models import PROJECT_CREATED
from meinberlin.apps.adminlog.models import LogEntry
from meinberlin.apps.ideas.phases import CollectPhase
from meinberlin.apps.projects.models import ProjectInsight
from meinberlin.apps.projects.tasks import send_publish_results_reminders
from meinberlin.apps.projects.utils import get_publish_results_reminder_initiators
from meinberlin.test.factories import UserFactory


def _add_adminlog_entry(project, actor, action=PROJECT_CREATED):
    LogEntry.objects.create(
        project=project,
        actor=actor,
        action=action,
        message="test",
        component_identifier="",
    )


def _prepare_eligible_project(phase, project):
    project.result = ""
    project.save()

    now = timezone.now()
    phase.start_date = now - timedelta(days=5)
    phase.end_date = now - timedelta(hours=2)
    phase.save()

    initiator = project.organisation.initiators.first()
    _add_adminlog_entry(project, initiator)
    return initiator


@pytest.mark.django_db
@override_settings(
    RESULTS_PUBLISH_REMINDER_DELAY_HOURS=0,
    RESULTS_PUBLISH_REMINDER_MIN_LAST_PARTICIPATION_END=None,
)
def test_send_publish_results_reminder_sends_email(phase_factory):
    phase, module, project, _item = setup_phase(phase_factory, None, CollectPhase)
    initiator = _prepare_eligible_project(phase, project)

    assert not mail.outbox
    send_publish_results_reminders()
    assert len(mail.outbox) == 1
    subject = mail.outbox[0].subject
    assert "Ergebnisse" in subject or "results" in subject.lower()
    assert mail.outbox[0].to[0] == initiator.email

    insight = ProjectInsight.objects.get(project=project)
    assert insight.results_reminder_sent_at is not None


@pytest.mark.django_db
@override_settings(
    RESULTS_PUBLISH_REMINDER_DELAY_HOURS=0,
    RESULTS_PUBLISH_REMINDER_MIN_LAST_PARTICIPATION_END=None,
)
def test_send_publish_results_reminder_skips_when_results_present(phase_factory):
    phase, module, project, _item = setup_phase(phase_factory, None, CollectPhase)
    project.result = "<p>Some results</p>"
    project.save()

    now = timezone.now()
    phase.start_date = now - timedelta(days=5)
    phase.end_date = now - timedelta(hours=2)
    phase.save()

    send_publish_results_reminders()
    assert len(mail.outbox) == 0


@pytest.mark.django_db
@override_settings(
    RESULTS_PUBLISH_REMINDER_DELAY_HOURS=0,
    RESULTS_PUBLISH_REMINDER_MIN_LAST_PARTICIPATION_END=None,
)
def test_send_publish_results_reminder_sends_for_offline_event_only_project(
    phase_factory,
):
    """Offline-event modules (OE) contribute phase end dates like other non-draft modules."""
    phase = phase_factory(module__blueprint_type="OE")
    project = phase.module.project
    _prepare_eligible_project(phase, project)

    assert not mail.outbox
    send_publish_results_reminders()
    assert len(mail.outbox) == 1

    insight = ProjectInsight.objects.get(project=project)
    assert insight.results_reminder_sent_at is not None


@pytest.mark.django_db
def test_send_publish_results_reminder_skips_when_last_end_before_min_cutoff(
    phase_factory,
):
    phase, module, project, _item = setup_phase(phase_factory, None, CollectPhase)
    project.result = ""
    project.save()

    now = timezone.now()
    phase.start_date = now - timedelta(days=5)
    phase.end_date = now - timedelta(hours=2)
    phase.save()

    min_cutoff = now - timedelta(hours=1)
    with override_settings(
        RESULTS_PUBLISH_REMINDER_DELAY_HOURS=0,
        RESULTS_PUBLISH_REMINDER_MIN_LAST_PARTICIPATION_END=min_cutoff,
    ):
        send_publish_results_reminders()
    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_send_publish_results_reminder_sends_when_last_end_on_or_after_min_cutoff(
    phase_factory,
):
    phase, module, project, _item = setup_phase(phase_factory, None, CollectPhase)
    _prepare_eligible_project(phase, project)

    min_cutoff = timezone.now() - timedelta(days=10)
    with override_settings(
        RESULTS_PUBLISH_REMINDER_DELAY_HOURS=0,
        RESULTS_PUBLISH_REMINDER_MIN_LAST_PARTICIPATION_END=min_cutoff,
    ):
        send_publish_results_reminders()
    assert len(mail.outbox) == 1


@pytest.mark.django_db
@override_settings(
    RESULTS_PUBLISH_REMINDER_DELAY_HOURS=168,
    RESULTS_PUBLISH_REMINDER_MIN_LAST_PARTICIPATION_END=None,
)
def test_send_publish_results_reminder_respects_delay(phase_factory):
    phase, module, project, _item = setup_phase(phase_factory, None, CollectPhase)
    project.result = ""
    project.save()

    now = timezone.now()
    phase.start_date = now - timedelta(days=5)
    phase.end_date = now - timedelta(hours=2)
    phase.save()

    send_publish_results_reminders()
    assert len(mail.outbox) == 0


@pytest.mark.django_db
@override_settings(
    RESULTS_PUBLISH_REMINDER_DELAY_HOURS=0,
    RESULTS_PUBLISH_REMINDER_MIN_LAST_PARTICIPATION_END=None,
)
def test_send_publish_results_reminder_only_to_involved_initiator(phase_factory):
    phase, module, project, _item = setup_phase(phase_factory, None, CollectPhase)
    _prepare_eligible_project(phase, project)

    uninvolved_initiator = UserFactory()
    project.organisation.initiators.add(uninvolved_initiator)

    send_publish_results_reminders()
    assert len(mail.outbox) == 1
    recipients = [email.to[0] for email in mail.outbox]
    assert uninvolved_initiator.email not in recipients


@pytest.mark.django_db
@override_settings(
    RESULTS_PUBLISH_REMINDER_DELAY_HOURS=0,
    RESULTS_PUBLISH_REMINDER_MIN_LAST_PARTICIPATION_END=None,
)
def test_send_publish_results_reminder_to_all_involved_initiators(phase_factory):
    phase, module, project, _item = setup_phase(phase_factory, None, CollectPhase)
    _prepare_eligible_project(phase, project)

    second_initiator = UserFactory()
    project.organisation.initiators.add(second_initiator)
    _add_adminlog_entry(project, second_initiator)

    send_publish_results_reminders()
    assert len(mail.outbox) == 2
    recipients = {email.to[0] for email in mail.outbox}
    assert project.organisation.initiators.filter(email__in=recipients).count() == 2


@pytest.mark.django_db
@override_settings(
    RESULTS_PUBLISH_REMINDER_DELAY_HOURS=0,
    RESULTS_PUBLISH_REMINDER_MIN_LAST_PARTICIPATION_END=None,
)
def test_send_publish_results_reminder_skips_initiator_without_adminlog(phase_factory):
    phase, module, project, _item = setup_phase(phase_factory, None, CollectPhase)
    _prepare_eligible_project(phase, project)

    project.organisation.initiators.clear()
    uninvolved_initiator = UserFactory()
    project.organisation.initiators.add(uninvolved_initiator)

    send_publish_results_reminders()
    assert len(mail.outbox) == 0

    insight = ProjectInsight.objects.get(project=project)
    assert insight.results_reminder_sent_at is not None


@pytest.mark.django_db
@override_settings(
    RESULTS_PUBLISH_REMINDER_DELAY_HOURS=0,
    RESULTS_PUBLISH_REMINDER_MIN_LAST_PARTICIPATION_END=None,
)
def test_send_publish_results_reminder_excludes_non_initiator_in_adminlog(
    phase_factory,
):
    phase, module, project, _item = setup_phase(phase_factory, None, CollectPhase)
    initiator = _prepare_eligible_project(phase, project)

    non_initiator = project.moderators.first()
    assert non_initiator not in project.organisation.initiators.all()
    _add_adminlog_entry(project, non_initiator)

    send_publish_results_reminders()
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to[0] == initiator.email


@pytest.mark.django_db
@override_settings(
    RESULTS_PUBLISH_REMINDER_DELAY_HOURS=0,
    RESULTS_PUBLISH_REMINDER_MIN_LAST_PARTICIPATION_END=None,
)
def test_send_publish_results_reminder_includes_initiator_with_component_update(
    phase_factory,
):
    phase, module, project, _item = setup_phase(phase_factory, None, CollectPhase)
    _prepare_eligible_project(phase, project)

    initiator = project.organisation.initiators.first()
    LogEntry.objects.filter(project=project, actor=initiator).delete()
    _add_adminlog_entry(project, initiator, action=PROJECT_COMPONENT_UPDATED)

    send_publish_results_reminders()
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to[0] == initiator.email


@pytest.mark.django_db
@override_settings(
    RESULTS_PUBLISH_REMINDER_DELAY_HOURS=0,
    RESULTS_PUBLISH_REMINDER_MIN_LAST_PARTICIPATION_END=None,
)
def test_send_publish_results_reminder_respects_notification_settings(phase_factory):
    phase, module, project, _item = setup_phase(phase_factory, None, CollectPhase)
    initiator = _prepare_eligible_project(phase, project)

    initiator.notification_settings.notify_initiators_publish_results = False
    initiator.notification_settings.save()

    send_publish_results_reminders()
    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_get_publish_results_reminder_initiators(phase_factory):
    phase, module, project, _item = setup_phase(phase_factory, None, CollectPhase)
    initiator = project.organisation.initiators.first()
    uninvolved_initiator = UserFactory()
    project.organisation.initiators.add(uninvolved_initiator)
    _add_adminlog_entry(project, initiator)

    involved = get_publish_results_reminder_initiators(project)
    assert list(involved) == [initiator]
