import pytest
from dateutil.parser import parse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from freezegun import freeze_time

from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from adhocracy4.test.helpers import setup_users
from meinberlin.apps.ideas import phases


@pytest.mark.django_db
def test_idea_list_filter_mixin(
    apiclient,
    user_factory,
    group_factory,
    phase_factory,
    idea_factory,
    category_factory,
    category_alias_factory,
    label_factory,
    label_alias_factory,
    moderation_task_factory,
):
    collect_phase, module, project, idea = setup_phase(
        phase_factory, idea_factory, phases.CollectPhase
    )
    user = user_factory()
    anonymous, moderator, initiator = setup_users(project)

    group_pro = group_factory()
    project.group = group_pro
    project.save()
    group_member = user_factory.create(groups=(group_pro,))

    category1 = category_factory(module=module)
    category2 = category_factory(module=module)

    moderation_task = moderation_task_factory(module=module)

    url = reverse("ideas-list", kwargs={"module_pk": module.pk})

    response = apiclient.get(url)

    # filter info
    assert "filters" in response.data
    assert len(response.data["filters"]) == 3

    assert "category" in response.data["filters"]
    assert response.data["filters"]["category"]["label"] == _("Category")
    assert response.data["filters"]["category"]["choices"][0] == ("", _("All"))
    assert (str(category1.pk), category1.name) in response.data["filters"]["category"][
        "choices"
    ]
    assert (str(category2.pk), category2.name) in response.data["filters"]["category"][
        "choices"
    ]
    # with category alias
    category_alias = category_alias_factory(module=module)
    response = apiclient.get(url)
    assert "category" in response.data["filters"]
    assert response.data["filters"]["category"]["label"] == category_alias.title

    assert "moderator_status" in response.data["filters"]
    assert response.data["filters"]["moderator_status"]["label"] == _("Status")
    assert response.data["filters"]["moderator_status"]["choices"] == [
        ("", _("All")),
        ("CONSIDERATION", _("Under consideration")),
        ("QUALIFIED", _("Qualified for next phase")),
        ("REJECTED", _("Rejected")),
        ("ACCEPTED", _("Accepted")),
    ]

    assert "ordering" in response.data["filters"]
    assert response.data["filters"]["ordering"]["label"] == _("Ordering")
    assert "labels" not in response.data["filters"]

    # with labels
    label1 = label_factory(module=module)
    label2 = label_factory(module=module)
    response = apiclient.get(url)
    assert "filters" in response.data
    assert len(response.data["filters"]) == 4
    assert "labels" in response.data["filters"]
    assert response.data["filters"]["labels"]["label"] == _("Label")
    assert (str(label1.pk), label1.name) in response.data["filters"]["labels"][
        "choices"
    ]
    assert (str(label2.pk), label2.name) in response.data["filters"]["labels"][
        "choices"
    ]
    # with label_alias
    label_alias = label_alias_factory(module=module)
    response = apiclient.get(url)
    assert "labels" in response.data["filters"]
    assert response.data["filters"]["labels"]["label"] == label_alias.title

    # ordering choices in different phases

    # module has already finished without freeze_time
    assert response.data["filters"]["ordering"]["choices"] == [
        ("-created", _("Most recent")),
        ("-comment_count", _("Most commented")),
        ("dailyrandom", _("Random")),
    ]
    assert response.data["filters"]["ordering"]["default"] == "dailyrandom"

    with freeze_phase(collect_phase):
        response = apiclient.get(url)
    assert response.data["filters"]["ordering"]["choices"] == [
        ("-created", _("Most recent")),
        ("-comment_count", _("Most commented")),
        ("dailyrandom", _("Random")),
    ]
    assert response.data["filters"]["ordering"]["default"] == "dailyrandom"

    # moderation tasks filter only added for moderators
    assert "open_task" not in response.data["filters"]

    apiclient.force_authenticate(user=user)
    response = apiclient.get(url)
    assert "open_task" not in response.data["filters"]

    apiclient.force_authenticate(user=moderator)
    response = apiclient.get(url)
    assert "open_task" in response.data["filters"]
    assert response.data["filters"]["open_task"]["choices"] == [
        ("", _("All")),
        (str(moderation_task.pk), moderation_task.name),
    ]

    apiclient.force_authenticate(user=initiator)
    response = apiclient.get(url)
    assert "open_task" in response.data["filters"]
    assert response.data["filters"]["open_task"]["choices"] == [
        ("", _("All")),
        (str(moderation_task.pk), moderation_task.name),
    ]

    apiclient.force_authenticate(user=group_member)
    response = apiclient.get(url)
    assert "open_task" in response.data["filters"]
    assert response.data["filters"]["open_task"]["choices"] == [
        ("", _("All")),
        (str(moderation_task.pk), moderation_task.name),
    ]


@pytest.mark.django_db
def test_idea_category_filter(
    apiclient, module, idea_factory, category_factory, phase_factory
):
    phase_factory(phase_content=phases.CollectPhase(), module=module)

    category1 = category_factory(module=module)
    category2 = category_factory(module=module)

    idea_cat1 = idea_factory(module=module, category=category1)
    idea_factory(module=module, category=category2)
    idea_factory(module=module, category=category2)

    url = reverse("ideas-list", kwargs={"module_pk": module.pk})

    response = apiclient.get(url)
    assert len(response.data["results"]) == 3

    querystring = "?category=" + str(category1.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == idea_cat1.pk

    querystring = "?category=" + str(category2.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_idea_category_alias_filter(
    apiclient,
    module,
    idea_factory,
    category_factory,
    category_alias_factory,
    phase_factory,
):
    phase_factory(phase_content=phases.CollectPhase(), module=module)

    category_alias = category_alias_factory(module=module)
    category1 = category_factory(module=module)
    category2 = category_factory(module=module)

    idea_cat1 = idea_factory(module=module, category=category1)
    idea_factory(module=module, category=category2)
    idea_factory(module=module, category=category2)

    url = reverse("ideas-list", kwargs={"module_pk": module.pk})

    response = apiclient.get(url)
    "category" in response.data["filters"]
    assert response.data["filters"]["category"]["label"] == category_alias.title

    assert len(response.data["results"]) == 3

    querystring = "?category=" + str(category1.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == idea_cat1.pk

    querystring = "?category=" + str(category2.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_idea_label_filter(
    apiclient, module, idea_factory, label_factory, phase_factory
):
    phase_factory(phase_content=phases.CollectPhase(), module=module)

    label1 = label_factory(module=module)
    label2 = label_factory(module=module)

    idea_1 = idea_factory(module=module)
    idea_1.labels.set([label1])
    idea_2 = idea_factory(module=module)
    idea_2.labels.set([label1, label2])
    idea_factory(module=module)

    url = reverse("ideas-list", kwargs={"module_pk": module.pk})

    response = apiclient.get(url)
    assert len(response.data["results"]) == 3

    querystring = "?labels=" + str(label1.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 2

    querystring = "?labels=" + str(label2.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == idea_2.pk


@pytest.mark.django_db
def test_idea_moderator_status_filter(apiclient, module, idea_factory, phase_factory):
    phase_factory(phase_content=phases.CollectPhase(), module=module)

    idea_factory(module=module, moderator_status="")
    idea_2 = idea_factory(module=module, moderator_status="CONSIDERATION")
    idea_3 = idea_factory(module=module, moderator_status="QUALIFIED")
    idea_4 = idea_factory(module=module, moderator_status="REJECTED")
    idea_5 = idea_factory(module=module, moderator_status="ACCEPTED")

    url = reverse("ideas-list", kwargs={"module_pk": module.pk})

    response = apiclient.get(url)
    assert len(response.data["results"]) == 5

    querystring = "?moderator_status=CONSIDERATION"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == idea_2.pk

    querystring = "?moderator_status=QUALIFIED"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == idea_3.pk

    querystring = "?moderator_status=REJECTED"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == idea_4.pk

    querystring = "?moderator_status=ACCEPTED"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == idea_5.pk


@pytest.mark.django_db
def test_idea_search_filter(apiclient, module, idea_factory, phase_factory):
    phase_factory(phase_content=phases.CollectPhase(), module=module)

    now = parse("2022-01-02 18:00:00 UTC")
    yesterday = now - timezone.timedelta(days=1)
    last_week = now - timezone.timedelta(days=7)

    idea_1 = idea_factory(pk=1, module=module, name="liqd idea", created=now)
    idea_factory(pk=2, module=module, name="other idea", created=last_week)
    idea_2 = idea_factory(
        pk=3, module=module, name="liqd has good ideas", created=yesterday
    )
    idea_factory(pk=4, module=module, name="idea from 2021", created=yesterday)
    idea_5 = idea_factory(pk=5, module=module, name="blabla", created=yesterday)

    url = reverse("ideas-list", kwargs={"module_pk": module.pk})

    response = apiclient.get(url)
    assert len(response.data["results"]) == 5

    querystring = "?search=liqd+idea"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 2
    assert response.data["results"][0]["pk"] == idea_2.pk
    assert response.data["results"][1]["pk"] == idea_1.pk

    querystring = "?search=liqd"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 2

    querystring = "?search=2021"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 2

    querystring = "?search=2021-00"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1

    querystring = "?search=2022-"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 4

    querystring = "?search=2022-00005"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == idea_5.pk

    querystring = "?search="
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 5


@pytest.mark.django_db
def test_ideas_ordering_filter(
    apiclient,
    module,
    idea_factory,
    comment_factory,
    rating_factory,
    phase_factory,
):
    phase_factory(phase_content=phases.CollectFeedbackPhase(), module=module)

    now = parse("2022-01-01 18:00:00 UTC")
    yesterday = now - timezone.timedelta(days=1)
    last_week = now - timezone.timedelta(days=7)

    idea_new = idea_factory(pk=1, module=module, created=now)
    idea_old = idea_factory(pk=2, module=module, created=last_week, name="liqd idea")

    idea_factory(pk=3, module=module, created=yesterday)
    idea_popular = idea_factory(pk=4, module=module, created=yesterday)
    rating_factory(content_object=idea_popular)
    rating_factory(content_object=idea_popular)

    idea_commented = idea_factory(pk=5, module=module, created=yesterday)
    comment_factory(content_object=idea_commented)

    idea_factory(pk=6, module=module, created=yesterday)

    idea_2_popular = idea_factory(pk=7, module=module, created=yesterday)
    rating_factory(content_object=idea_2_popular)

    idea_factory(pk=8, module=module, created=yesterday)

    url = reverse("ideas-list", kwargs={"module_pk": module.pk})

    # queryset is ordered by created
    querystring = "?ordering=-created"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 8
    assert response.data["results"][0]["pk"] == idea_new.pk
    assert response.data["results"][-1]["pk"] == idea_old.pk

    # positive rating
    querystring = "?ordering=-positive_rating_count"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 8
    assert response.data["results"][0]["pk"] == idea_popular.pk
    assert response.data["results"][1]["pk"] == idea_2_popular.pk

    # most commented
    querystring = "?ordering=-comment_count"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 8
    assert response.data["results"][0]["pk"] == idea_commented.pk

    # daily random
    querystring = "?ordering=dailyrandom"
    url_tmp = url + querystring
    with freeze_time("2020-01-01 00:00:00 UTC"):
        response = apiclient.get(url_tmp)
    ordered_pks = [idea["pk"] for idea in response.data["results"]]
    assert ordered_pks == [6, 8, 7, 2, 1, 3, 4, 5]
    with freeze_time("2022-01-01 00:00:00 UTC"):
        response = apiclient.get(url_tmp)
    ordered_pks = [idea["pk"] for idea in response.data["results"]]
    assert ordered_pks == [8, 2, 4, 7, 6, 5, 1, 3]


@pytest.mark.django_db
def test_ideas_default_ordering_filter(
    apiclient,
    module,
    phase_factory,
    idea_factory,
    rating_factory,
):
    collect_phase = phase_factory(
        phase_content=phases.CollectPhase(),
        module=module,
        start_date=parse("2022-01-01 00:00:00 UTC"),
        end_date=parse("2022-01-01 10:00:00 UTC"),
    )
    voting_phase = phase_factory(
        phase_content=phases.FeedbackPhase(),
        module=module,
        start_date=parse("2022-01-01 14:00:00 UTC"),
        end_date=parse("2022-01-01 18:00:00 UTC"),
    )

    between_phases = parse("2022-01-01 12:00:00 UTC")
    module_ended = parse("2022-01-01 19:00:00 UTC")

    url = reverse("ideas-list", kwargs={"module_pk": module.pk})

    idea_factory(pk=1, module=module)
    idea_2 = idea_factory(pk=2, module=module)
    idea_3 = idea_factory(pk=3, module=module)

    rating_factory(content_object=idea_2, value=1)
    rating_factory(content_object=idea_2, value=1)
    rating_factory(content_object=idea_3, value=1)

    # dailyrandom is default during collect
    # dailyrandom order for '2022-01-01' is [2, 1, 3]
    with freeze_phase(collect_phase):
        response = apiclient.get(url)
    ordered_pks = [idea["pk"] for idea in response.data["results"]]
    assert ordered_pks == [2, 1, 3]

    # dailyrandom is default between collect and feedback
    with freeze_time(between_phases):
        response = apiclient.get(url)
    ordered_pks = [idea["pk"] for idea in response.data["results"]]
    assert ordered_pks == [2, 1, 3]

    # dailyrandom is default during feedback
    with freeze_phase(voting_phase):
        response = apiclient.get(url)
    ordered_pks = [idea["pk"] for idea in response.data["results"]]
    assert ordered_pks == [2, 1, 3]

    # daily_random is default after phases have ended
    with freeze_time(module_ended):
        response = apiclient.get(url)
    ordered_pks = [idea["pk"] for idea in response.data["results"]]
    assert ordered_pks == [2, 1, 3]


@pytest.mark.django_db
def test_idea_filter_combinations(
    apiclient,
    module,
    idea_factory,
    category_factory,
    comment_factory,
    rating_factory,
    label_factory,
    phase_factory,
):
    phase_factory(phase_content=phases.CollectFeedbackPhase(), module=module)

    category1 = category_factory(module=module)
    category2 = category_factory(module=module)
    label1 = label_factory(module=module)
    label2 = label_factory(module=module)

    now = parse("2022-01-01 18:00:00 UTC")
    yesterday = now - timezone.timedelta(days=1)
    last_week = now - timezone.timedelta(days=7)

    idea_now = idea_factory(pk=1, module=module, created=now)
    idea_factory(pk=2, module=module, created=last_week, name="liqd idea")

    idea_popular_labels = idea_factory(pk=4, module=module, created=yesterday)
    idea_popular_labels.labels.set([label1, label2])
    rating_factory(content_object=idea_popular_labels)
    rating_factory(content_object=idea_popular_labels)

    idea_commented = idea_factory(pk=5, module=module, created=yesterday)
    comment_factory(content_object=idea_commented)

    idea_factory(pk=6, module=module, created=yesterday, category=category1)

    idea_cat2_popular = idea_factory(
        pk=7, module=module, created=yesterday, category=category2
    )
    rating_factory(content_object=idea_cat2_popular)

    url = reverse("ideas-list", kwargs={"module_pk": module.pk})

    # combinations
    querystring = "?category=" + str(category2.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == idea_cat2_popular.pk

    querystring = "?search=2022-"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == idea_now.pk

    querystring = "?ordering=-created&search=2021-"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 5

    querystring = "?ordering=-positive_rating_count&labels=" + str(label1.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == idea_popular_labels.pk

    querystring = "?ordering=dailyrandom&category=" + str(category2.pk)
    url_tmp = url + querystring
    with freeze_time("2020-01-01 00:00:00 UTC"):
        response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == idea_cat2_popular.pk
