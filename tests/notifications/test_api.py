import pytest
from rest_framework.reverse import reverse

from adhocracy4.dashboard import signals
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.ideas import phases
from meinberlin.apps.notifications.models import Notification
from meinberlin.test.factories import CommentFactory


@pytest.mark.django_db
def test_shows_notification_for_remark(
    apiclient, user, idea_factory, moderator_remark_factory
):
    idea = idea_factory(creator=user)
    moderator_remark_factory(item=idea)
    apiclient.force_authenticate(user=user)
    url = reverse("notifications-list")
    response = apiclient.get(url)
    notification = response.data["results"][0]
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert notification["action"]["type"] == "moderatorremark"
    assert not notification["read"]


@pytest.mark.django_db
def test_shows_notification_for_comment(apiclient, user, idea_factory, comment_factory):
    idea = idea_factory(creator=user)
    comment_factory(content_object=idea)
    apiclient.force_authenticate(user=user)
    url = reverse("notifications-list")
    response = apiclient.get(url)
    notification = response.data["results"][0]
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert notification["action"]["type"] == "comment"


@pytest.mark.django_db
def test_shows_notification_for_rating(apiclient, user, idea_factory, rating_factory):
    idea = idea_factory(creator=user)
    rating_factory(content_object=idea)
    apiclient.force_authenticate(user=user)
    url = reverse("notifications-list")
    response = apiclient.get(url)
    notification = response.data["results"][0]
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert notification["action"]["type"] == "rating"


@pytest.mark.django_db
def test_doesnt_show_notification_for_own_action(
    apiclient, user, idea_factory, comment_factory
):
    idea = idea_factory(creator=user)
    comment_factory(content_object=idea, creator=user)
    apiclient.force_authenticate(user=user)
    url = reverse("notifications-list")
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 0


@pytest.mark.django_db
def test_doesnt_show_notification_for_other_users(
    apiclient, user, user2, idea_factory, comment_factory
):
    idea = idea_factory(creator=user2)
    comment_factory(content_object=idea, creator=user)
    apiclient.force_authenticate(user=user)
    url = reverse("notifications-list")
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 0


@pytest.mark.django_db
def test_interactions_basic_elements(
    apiclient,
    user,
    idea_factory,
    comment_factory,
    rating_factory,
    moderator_remark_factory,
):
    idea = idea_factory(creator=user)
    comment_factory(content_object=idea)
    rating_factory(content_object=idea)
    moderator_remark_factory(item=idea)
    apiclient.force_authenticate(user=user)
    url = reverse("notifications-interactions")
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 3
    assert response.data["results"][0]["action"]["type"] == "moderatorremark"
    assert response.data["results"][1]["action"]["type"] == "rating"
    assert response.data["results"][2]["action"]["type"] == "comment"


@pytest.mark.django_db
def test_interactions_aggregated_rating(apiclient, user, idea_factory, rating_factory):
    idea = idea_factory(creator=user)
    rating_factory(content_object=idea)
    rating_factory(content_object=idea)
    rating_factory(content_object=idea)
    rating_factory(content_object=idea)
    apiclient.force_authenticate(user=user)
    url = reverse("notifications-interactions")
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    notification = response.data["results"][0]
    assert notification["action"]["type"] == "rating"
    assert notification["total_ratings"] == 4


@pytest.mark.django_db
def test_interactions_mark_all_as_read(apiclient, user, idea_factory):
    idea = idea_factory(creator=user)
    CommentFactory.create_batch(10, content_object=idea)
    apiclient.force_authenticate(user=user)
    url = reverse("notifications-interactions")

    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 10
    for notification in response.data["results"]:
        assert not notification["read"]

    response = apiclient.post(url, {"read": True})
    assert response.status_code == 200
    for notification in response.data["results"]:
        assert notification["read"]


@pytest.mark.django_db
def test_interactions_mark_single_as_read(
    apiclient, user, idea_factory, comment_factory
):
    idea = idea_factory(creator=user)
    comment_factory(content_object=idea)

    notifications = Notification.objects.all()
    assert notifications.exists(), "No notification was created"
    notification = notifications.first()
    assert notification.read_at is None

    notification = Notification.objects.filter(recipient=user).first()
    assert notification.read_at is None
    url = reverse("notifications-detail", args=[notification.pk])

    apiclient.force_authenticate(user=user)
    response = apiclient.patch(url, {"read": True})
    assert response.status_code == 200
    assert response.data["read"]


@pytest.mark.django_db
def test_search_profiles(apiclient, user, phase_factory, search_factories):
    matching_profile, non_matching_profile_same_user, matching_profile_other_user = (
        search_factories
    )

    phase, module, project, _ = setup_phase(
        phase_factory, None, phases.CollectPhase, module__project__name="Berlin"
    )
    signals.project_published.send(sender=None, project=project, user=user)

    apiclient.force_authenticate(user=user)
    url = reverse("notifications-search-profiles")
    response = apiclient.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["action"]["type"] == "project_published"
    assert response.data["results"][0]["search_profile"]["id"] == matching_profile.id
