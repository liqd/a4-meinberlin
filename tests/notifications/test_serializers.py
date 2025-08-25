import pytest
from django.db.models import Count
from django.utils import timezone
from freezegun import freeze_time

from adhocracy4.actions.signals import _add_action
from adhocracy4.notifications.models import Notification
from meinberlin.apps.notifications.serializers import NotificationSerializer


@pytest.mark.django_db
def test_notification_serializer_representation(
    idea_factory, comment_factory, rating_factory
):
    comment = comment_factory(content_object=idea_factory())
    rating = rating_factory(content_object=comment)
    _add_action(None, rating, True, None)

    annotated_notification = Notification.objects.annotate(
        total_ratings=Count("action")
    ).first()
    serializer = NotificationSerializer(annotated_notification)
    assert "total_ratings" in serializer.data
    assert serializer.data["total_ratings"] == 1

    normal_notification = Notification.objects.first()
    serializer = NotificationSerializer(normal_notification)
    assert "total_ratings" not in serializer.data


@pytest.mark.django_db
def test_notification_serializer_save(idea_factory, comment_factory, rating_factory):
    comment = comment_factory(content_object=idea_factory())
    rating = rating_factory(content_object=comment)
    _add_action(None, rating, True, None)

    notification = Notification.objects.first()
    assert notification.read_at is None
    serializer = NotificationSerializer(notification, {"read": True})
    serializer.is_valid()
    assert serializer.is_valid()

    with freeze_time("2020-01-01"):
        serializer.save()
        assert notification.read_at == timezone.now()
        assert notification.read
