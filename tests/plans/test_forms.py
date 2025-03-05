import pytest

from adhocracy4.images.validators import ImageAltTextValidator
from adhocracy4.projects.models import Topic
from meinberlin.apps.plans.forms import PlanForm


@pytest.mark.django_db
def test_plan_form_metadata_required(organisation, plan_factory, ImagePNG):
    plan = plan_factory(organisation=organisation, image=ImagePNG, tile_image=ImagePNG)
    form = PlanForm(
        instance=plan,
        data={
            "title": "my changed title",
        },
    )
    assert not form.is_valid()
    assert "image_copyright" in form.errors
    assert "image_alt_text" in form.errors
    assert "tile_image_copyright" in form.errors
    assert "tile_image_alt_text" in form.errors


@pytest.mark.django_db
def test_plan_form_missing_alt_text(organisation, plan_factory):
    plan = plan_factory(organisation=organisation)
    form = PlanForm(
        instance=plan,
        data={
            "description": "description <img>",
        },
    )
    assert not form.is_valid()
    assert "description" in form.errors
    assert (
        form.errors["description"].data[0].messages[0] == ImageAltTextValidator.message
    )


@pytest.mark.django_db
def test_plan_form_with_point_as_dict_and_alt_text(
    organisation, plan_factory, geojson_point, administrative_district_factory
):
    plan = plan_factory(organisation=organisation)
    district = administrative_district_factory()
    form = PlanForm(
        instance=plan,
        data={
            "title": "title",
            "description": 'description <img alt="description">',
            "point": geojson_point,
            "point_label": "somewhere",
            "cost": "500",
            "topics": [Topic.objects.first()],
            "status": "0",
            "participation": "0",
            "participation_explanation": "exp",
            "district": district.id,
        },
    )
    assert "description" not in form.errors
    assert form.is_valid()


@pytest.mark.django_db
def test_plan_form_with_point_as_str_and_alt_text(
    organisation, plan_factory, geojson_point_str, administrative_district_factory
):
    plan = plan_factory(organisation=organisation)
    district = administrative_district_factory()
    form = PlanForm(
        instance=plan,
        data={
            "title": "title",
            "description": 'description <img alt="description">',
            "point": geojson_point_str,
            "point_label": "somewhere else",
            "cost": "500",
            "topics": [Topic.objects.first()],
            "status": "0",
            "participation": "0",
            "participation_explanation": "exp",
            "district": district.id,
        },
    )
    assert "description" not in form.errors
    assert form.is_valid()
