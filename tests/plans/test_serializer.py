import pytest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from freezegun import freeze_time

from meinberlin.apps.plans.models import Plan
from meinberlin.apps.plans.serializers import PlanSerializer


@pytest.mark.django_db
def test_serializer(
    client,
    plan_factory,
    project_factory,
    phase_factory,
    ImagePNG,
    geos_point,
    geojson_point,
):
    project1 = project_factory()
    project2 = project_factory()
    project3 = project_factory(is_draft=True)
    project4 = project_factory()
    project5 = project_factory()

    now = timezone.now()
    yesterday = now - timezone.timedelta(days=1)
    next_week = now - timezone.timedelta(days=7)
    tomorrow = now + timezone.timedelta(days=1)
    last_week = now - timezone.timedelta(days=7)

    phase_factory(
        start_date=yesterday,
        end_date=tomorrow,
        module__project=project1,
    )

    phase_factory(
        start_date=tomorrow,
        end_date=next_week,
        module__project=project2,
    )

    phase_factory(
        start_date=yesterday,
        end_date=tomorrow,
        module__project=project4,
    )

    phase_factory(
        start_date=tomorrow,
        end_date=next_week,
        module__project=project4,
    )

    phase_factory(
        start_date=last_week,
        end_date=yesterday,
        module__project=project5,
    )

    with freeze_time(now):
        plan_factory.create(
            pk=1,
            projects=[project1],
            image=ImagePNG,
            image_copyright="copyright",
            image_alt_text="img_alt",
            point=geos_point,
        )
        plan_factory.create(
            pk=2,
            projects=[project2],
            tile_image=ImagePNG,
            tile_image_copyright="copyright",
            tile_image_alt_text="img_alt",
        )
        plan_factory.create(pk=3, projects=[project3], status=Plan.STATUS_DONE)
        plan_factory.create(pk=4, projects=[project4])
        plan_factory.create(pk=5, projects=[project5], status=Plan.STATUS_DONE)
        plans = Plan.objects.all().order_by("pk")

        plan_serializer = PlanSerializer(plans, many=True)
        plan_data = plan_serializer.data
        assert len(plan_data) == 5

        assert plan_data[0]["type"] == "plan"
        assert plan_data[1]["type"] == "plan"
        assert plan_data[2]["type"] == "plan"
        assert plan_data[3]["type"] == "plan"
        assert plan_data[4]["type"] == "plan"

        assert plan_data[0]["published_projects_count"] == 1
        assert plan_data[1]["published_projects_count"] == 1
        assert plan_data[2]["published_projects_count"] == 0
        assert plan_data[3]["published_projects_count"] == 1
        assert plan_data[4]["published_projects_count"] == 1

        assert plan_data[0]["participation_string"] == _("running")
        assert plan_data[1]["participation_string"] == _("running")
        assert plan_data[2]["participation_string"] == _("done")
        assert plan_data[3]["participation_string"] == _("running")
        assert plan_data[4]["participation_string"] == _("done")

        assert plan_data[0]["participation_active"]
        assert plan_data[1]["participation_active"]
        assert not plan_data[2]["participation_active"]
        assert plan_data[3]["participation_active"]
        assert not plan_data[4]["participation_active"]

        assert plan_data[0]["tile_image"]
        assert plan_data[1]["tile_image"]
        assert not plan_data[2]["tile_image"]
        assert not plan_data[3]["tile_image"]
        assert not plan_data[4]["tile_image"]

        assert plan_data[0]["tile_image_copyright"]
        assert plan_data[1]["tile_image_copyright"]
        assert not plan_data[2]["tile_image_copyright"]
        assert not plan_data[3]["tile_image_copyright"]
        assert not plan_data[4]["tile_image_copyright"]

        assert plan_data[0]["tile_image_alt_text"]
        assert plan_data[1]["tile_image_alt_text"]
        assert not plan_data[2]["tile_image_alt_text"]
        assert not plan_data[3]["tile_image_alt_text"]
        assert not plan_data[4]["tile_image_alt_text"]

        assert plan_data[0]["point"] == geojson_point
