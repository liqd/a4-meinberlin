import pytest

from meinberlin.apps.mapideas.forms import MapIdeaForm


@pytest.mark.django_db
def test_mapidea_form_with_contact_mixins(module, area_settings_factory):
    area_settings_factory(module=module)
    form = MapIdeaForm(module=module, settings_instance=module.settings_instance)
    fields = [
        "name",
        "description",
        "image",
        "category",
        "labels",
        "point",
        "point_label",
        "allow_contact",
        "contact_email",
        "contact_phone",
        "contact_storage_consent",
    ]

    for field in fields:
        assert field in form.fields
