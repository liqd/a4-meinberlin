import pytest
from freezegun import freeze_time

from adhocracy4.notifications.models import Notification
from meinberlin.apps.notifications.tasks import periodic_notifications_cleanup
from meinberlin.test.factories import CommentFactory


@pytest.mark.django_db
def test_notifications_deleted_after_180_days(idea_factory):
    with freeze_time("2020-01-01"):
        CommentFactory.create_batch(15, content_object=idea_factory())

    with freeze_time("2021-01-01"):
        CommentFactory.create_batch(10, content_object=idea_factory())

    with freeze_time("2021-03-01"):
        periodic_notifications_cleanup()

    assert Notification.objects.count() == 10
