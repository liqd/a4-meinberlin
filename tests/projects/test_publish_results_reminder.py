from datetime import timedelta

import pytest
from django.core import mail
from django.test.utils import override_settings
from django.utils import timezone

from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.ideas.phases import CollectPhase
from meinberlin.apps.projects.models import ProjectInsight
from meinberlin.apps.projects.tasks import send_publish_results_reminders


@pytest.mark.django_db
@override_settings(RESULTS_PUBLISH_REMINDER_DELAY_HOURS=0)
def test_send_publish_results_reminder_sends_email(phase_factory):
    phase, module, project, _item = setup_phase(phase_factory, None, CollectPhase)
    project.result = ""
    project.save()

    now = timezone.now()
    phase.start_date = now - timedelta(days=5)
    phase.end_date = now - timedelta(hours=2)
    phase.save()

    assert not mail.outbox
    send_publish_results_reminders()
    assert len(mail.outbox) == 1
    subject = mail.outbox[0].subject
    assert "Ergebnisse" in subject or "results" in subject.lower()
    assert project.organisation.initiators.filter(email=mail.outbox[0].to[0]).exists()

    insight = ProjectInsight.objects.get(project=project)
    assert insight.results_reminder_sent_at is not None


@pytest.mark.django_db
@override_settings(RESULTS_PUBLISH_REMINDER_DELAY_HOURS=0)
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
@override_settings(RESULTS_PUBLISH_REMINDER_DELAY_HOURS=168)
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
