import pytest
from dateutil.parser import parse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from freezegun import freeze_time

from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.topicprio import phases


@pytest.mark.django_db
def test_topic_list_filter_mixin(
    apiclient,
    group_factory,
    phase_factory,
    topic_factory,
    category_factory,
    category_alias_factory,
    label_factory,
    label_alias_factory,
):
    prioritize_phase, module, project, topic = setup_phase(
        phase_factory, topic_factory, phases.PrioritizePhase
    )

    group_pro = group_factory()
    project.group = group_pro
    project.save()

    category1 = category_factory(module=module)
    category2 = category_factory(module=module)

    url = reverse("topics-list", kwargs={"module_pk": module.pk})

    response = apiclient.get(url)

    # filter info
    assert "filters" in response.data
    assert len(response.data["filters"]) == 2

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

    assert "ordering" in response.data["filters"]
    assert response.data["filters"]["ordering"]["label"] == _("Ordering")
    assert "labels" not in response.data["filters"]

    # with labels
    label1 = label_factory(module=module)
    label2 = label_factory(module=module)
    response = apiclient.get(url)
    assert "filters" in response.data
    assert len(response.data["filters"]) == 3
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
        ("-comment_count", _("Most commented")),
        ("dailyrandom", _("Random")),
        ("-positive_rating_count", _("Most popular")),
    ]
    assert response.data["filters"]["ordering"]["default"] == "dailyrandom"

    with freeze_phase(prioritize_phase):
        response = apiclient.get(url)
    assert response.data["filters"]["ordering"]["choices"] == [
        ("-comment_count", _("Most commented")),
        ("dailyrandom", _("Random")),
        ("-positive_rating_count", _("Most popular")),
    ]
    assert response.data["filters"]["ordering"]["default"] == "dailyrandom"


@pytest.mark.django_db
def test_topic_category_filter(
    apiclient, module, topic_factory, category_factory, phase_factory
):
    phase_factory(phase_content=phases.PrioritizePhase(), module=module)

    category1 = category_factory(module=module)
    category2 = category_factory(module=module)

    topic_cat1 = topic_factory(module=module, category=category1)
    topic_factory(module=module, category=category2)
    topic_factory(module=module, category=category2)

    url = reverse("topics-list", kwargs={"module_pk": module.pk})

    response = apiclient.get(url)
    assert len(response.data["results"]) == 3

    querystring = "?category=" + str(category1.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == topic_cat1.pk

    querystring = "?category=" + str(category2.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_topic_category_alias_filter(
    apiclient,
    module,
    topic_factory,
    category_factory,
    category_alias_factory,
    phase_factory,
):
    phase_factory(phase_content=phases.PrioritizePhase(), module=module)

    category_alias = category_alias_factory(module=module)
    category1 = category_factory(module=module)
    category2 = category_factory(module=module)

    topic_cat1 = topic_factory(module=module, category=category1)
    topic_factory(module=module, category=category2)
    topic_factory(module=module, category=category2)

    url = reverse("topics-list", kwargs={"module_pk": module.pk})

    response = apiclient.get(url)
    "category" in response.data["filters"]
    assert response.data["filters"]["category"]["label"] == category_alias.title

    assert len(response.data["results"]) == 3

    querystring = "?category=" + str(category1.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == topic_cat1.pk

    querystring = "?category=" + str(category2.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_topic_label_filter(
    apiclient, module, topic_factory, label_factory, phase_factory
):
    phase_factory(phase_content=phases.PrioritizePhase(), module=module)

    label1 = label_factory(module=module)
    label2 = label_factory(module=module)

    topic_1 = topic_factory(module=module)
    topic_1.labels.set([label1])
    topic_2 = topic_factory(module=module)
    topic_2.labels.set([label1, label2])
    topic_factory(module=module)

    url = reverse("topics-list", kwargs={"module_pk": module.pk})

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
    assert response.data["results"][0]["pk"] == topic_2.pk


@pytest.mark.django_db
def test_topic_search_filter(apiclient, module, topic_factory, phase_factory):
    phase_factory(phase_content=phases.PrioritizePhase(), module=module)

    now = parse("2022-01-02 18:00:00 UTC")
    yesterday = now - timezone.timedelta(days=1)
    last_week = now - timezone.timedelta(days=7)

    topic_1 = topic_factory(pk=1, module=module, name="liqd topic", created=now)
    topic_factory(pk=2, module=module, name="other topic", created=last_week)
    topic_factory(
        pk=3, module=module, name="liqd has a lot of creativity", created=yesterday
    )
    topic_factory(pk=4, module=module, name="topic from 2021", created=yesterday)
    topic_factory(pk=5, module=module, name="blabla", created=yesterday)

    url = reverse("topics-list", kwargs={"module_pk": module.pk})

    response = apiclient.get(url)
    assert len(response.data["results"]) == 5

    querystring = "?search=liqd+topic"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == topic_1.pk

    querystring = "?search=liqd"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 2

    querystring = "?search=2021"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1

    querystring = "?search=2021-00"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 0

    querystring = "?search="
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 5


@pytest.mark.django_db
def test_topics_ordering_filter(
    apiclient,
    module,
    topic_factory,
    comment_factory,
    rating_factory,
    phase_factory,
):
    phase_factory(phase_content=phases.PrioritizePhase(), module=module)

    topic_factory(pk=3, module=module)
    topic_popular = topic_factory(pk=4, module=module)
    rating_factory(content_object=topic_popular)
    rating_factory(content_object=topic_popular)

    topic_commented = topic_factory(pk=5, module=module)
    comment_factory(content_object=topic_commented)

    topic_factory(pk=6, module=module)

    topic_2_popular = topic_factory(pk=7, module=module)
    rating_factory(content_object=topic_2_popular)

    topic_factory(pk=8, module=module)

    url = reverse("topics-list", kwargs={"module_pk": module.pk})

    # positive rating
    querystring = "?ordering=-positive_rating_count"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 6
    assert response.data["results"][0]["pk"] == topic_popular.pk
    assert response.data["results"][1]["pk"] == topic_2_popular.pk

    # most commented
    querystring = "?ordering=-comment_count"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 6
    assert response.data["results"][0]["pk"] == topic_commented.pk

    # daily random
    querystring = "?ordering=dailyrandom"
    url_tmp = url + querystring
    with freeze_time("2020-01-01 00:00:00 UTC"):
        response = apiclient.get(url_tmp)
    ordered_pks = [topic["pk"] for topic in response.data["results"]]
    assert ordered_pks == [4, 5, 8, 3, 6, 7]
    with freeze_time("2022-01-01 00:00:00 UTC"):
        response = apiclient.get(url_tmp)
    ordered_pks = [topic["pk"] for topic in response.data["results"]]
    assert ordered_pks == [4, 7, 6, 5, 3, 8]


@pytest.mark.django_db
def test_topics_default_ordering_filter(
    apiclient,
    module,
    phase_factory,
    topic_factory,
    rating_factory,
):
    prioritize_phase = phase_factory(
        phase_content=phases.PrioritizePhase(),
        module=module,
        start_date=parse("2022-01-01 00:00:00 UTC"),
        end_date=parse("2022-01-01 10:00:00 UTC"),
    )
    voting_phase = phase_factory(
        phase_content=phases.PrioritizePhase(),
        module=module,
        start_date=parse("2022-01-01 14:00:00 UTC"),
        end_date=parse("2022-01-01 18:00:00 UTC"),
    )

    between_phases = parse("2022-01-01 12:00:00 UTC")
    module_ended = parse("2022-01-01 19:00:00 UTC")

    url = reverse("topics-list", kwargs={"module_pk": module.pk})

    topic_factory(pk=1, module=module)
    topic_2 = topic_factory(pk=2, module=module)
    topic_3 = topic_factory(pk=3, module=module)

    rating_factory(content_object=topic_2, value=1)
    rating_factory(content_object=topic_2, value=1)
    rating_factory(content_object=topic_3, value=1)

    # dailyrandom is default during collect
    # dailyrandom order for '2022-01-01' is [2, 1, 3]
    with freeze_phase(prioritize_phase):
        response = apiclient.get(url)
    ordered_pks = [topic["pk"] for topic in response.data["results"]]
    assert ordered_pks == [2, 1, 3]

    # dailyrandom is default between collect and feedback
    with freeze_time(between_phases):
        response = apiclient.get(url)
    ordered_pks = [topic["pk"] for topic in response.data["results"]]
    assert ordered_pks == [2, 1, 3]

    # dailyrandom is default during feedback
    with freeze_phase(voting_phase):
        response = apiclient.get(url)
    ordered_pks = [topic["pk"] for topic in response.data["results"]]
    assert ordered_pks == [2, 1, 3]

    # daily_random is default after phases have ended
    with freeze_time(module_ended):
        response = apiclient.get(url)
    ordered_pks = [topic["pk"] for topic in response.data["results"]]
    assert ordered_pks == [2, 1, 3]


@pytest.mark.django_db
def test_topic_filter_combinations(
    apiclient,
    module,
    topic_factory,
    category_factory,
    comment_factory,
    rating_factory,
    label_factory,
    phase_factory,
):
    phase_factory(phase_content=phases.PrioritizePhase(), module=module)

    category1 = category_factory(module=module)
    category2 = category_factory(module=module)
    label1 = label_factory(module=module)
    label2 = label_factory(module=module)

    now = parse("2022-01-01 18:00:00 UTC")
    yesterday = now - timezone.timedelta(days=1)
    last_week = now - timezone.timedelta(days=7)

    topic_factory(pk=1, module=module, created=now)
    topic_factory(pk=2, module=module, created=last_week, name="liqd topic")

    topic_popular_labels = topic_factory(pk=4, module=module, created=yesterday)
    topic_popular_labels.labels.set([label1, label2])
    rating_factory(content_object=topic_popular_labels)
    rating_factory(content_object=topic_popular_labels)

    topic_commented = topic_factory(pk=5, module=module, created=yesterday)
    comment_factory(content_object=topic_commented)

    topic_factory(pk=6, module=module, created=yesterday, category=category1)

    topic_cat2_popular = topic_factory(
        pk=7, module=module, created=yesterday, category=category2
    )
    rating_factory(content_object=topic_cat2_popular)

    url = reverse("topics-list", kwargs={"module_pk": module.pk})

    # combinations
    querystring = "?category=" + str(category2.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == topic_cat2_popular.pk

    querystring = "?search=2022-"
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 0

    querystring = "?ordering=-positive_rating_count&labels=" + str(label1.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == topic_popular_labels.pk

    querystring = "?ordering=dailyrandom&category=" + str(category2.pk)
    url_tmp = url + querystring
    with freeze_time("2020-01-01 00:00:00 UTC"):
        response = apiclient.get(url_tmp)
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["pk"] == topic_cat2_popular.pk
