import re
from datetime import datetime
from datetime import timedelta
from typing import List
from typing import Optional

from django.conf import settings
from django.utils import timezone
from django.utils.html import strip_tags

from meinberlin.apps.dashboard import is_event_module


def html_field_has_meaningful_content(value: Optional[str]) -> bool:
    """True if a CKEditor/HTML field has non-whitespace text (matches template filter)."""
    if not value:
        return False
    text = strip_tags(value)
    text = re.sub(r"&nbsp;|\s", "", text)
    return len(text) > 0


def get_last_online_participation_end(project) -> Optional[datetime]:
    """
    Latest phase end among non-draft, online (non-event) modules.
    None if there is no such module or no dated phases.
    """
    end_candidates: List[datetime] = []
    for module in project.module_set.all():
        if module.is_draft or is_event_module(module):
            continue
        phase_ends = [
            p.end_date for p in module.phase_set.all() if p.end_date is not None
        ]
        if not phase_ends:
            continue
        end_candidates.append(max(phase_ends))
    if not end_candidates:
        return None
    return max(end_candidates)


def get_publish_results_reminder_skip_reason(
    project,
    *,
    now: Optional[datetime] = None,
) -> Optional[str]:
    """
    If the project would not receive the automatic publish-results reminder at ``now``,
    return a short reason code; otherwise return None (eligible).

    Possible codes: ``project_not_eligible``, ``reminder_already_sent``,
    ``result_has_content``, ``reminder_not_due`` (covers unfinished participation,
    minimum last-end cutoff, and delay-hours gate).

    Mirrors ``send_publish_results_reminders`` filters (same settings).
    """
    if now is None:
        now = timezone.now()

    if (
        project.project_type != "a4projects.Project"
        or project.is_draft
        or project.is_archived
    ):
        return "project_not_eligible"

    from meinberlin.apps.projects.models import ProjectInsight

    try:
        insight = project.insight
    except ProjectInsight.DoesNotExist:
        insight = None
    if insight and insight.results_reminder_sent_at is not None:
        return "reminder_already_sent"

    if html_field_has_meaningful_content(project.result):
        return "result_has_content"

    last_end = get_last_online_participation_end(project)
    if last_end is None or last_end > now:
        return "reminder_not_due"

    min_last_participation_end = getattr(
        settings,
        "RESULTS_PUBLISH_REMINDER_MIN_LAST_PARTICIPATION_END",
        None,
    )
    if min_last_participation_end is not None and last_end < min_last_participation_end:
        return "reminder_not_due"

    delay_hours: int = settings.RESULTS_PUBLISH_REMINDER_DELAY_HOURS
    threshold = last_end + timedelta(hours=delay_hours)
    if now < threshold:
        return "reminder_not_due"

    return None


def apply_publish_results_reminder(project, *, now: datetime) -> None:
    """
    Send the publish-results reminder and persist ``results_reminder_sent_at``.

    Caller must ensure the project is eligible (see ``get_publish_results_reminder_skip_reason``).
    """
    from meinberlin.apps.notifications import emails as notification_emails
    from meinberlin.apps.projects.models import ProjectInsight

    notification_emails.NotifyInitiatorsPublishResultsEmail.send(project)
    insight, _ = ProjectInsight.objects.get_or_create(project=project)
    insight.results_reminder_sent_at = now
    insight.save(update_fields=["results_reminder_sent_at"])
