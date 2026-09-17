import pytest

from meinberlin.apps.ideas.forms import IdeaForm
from meinberlin.apps.mapideas.forms import MapIdeaForm

POINT = {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "type": "Point",
        "coordinates": [13.447437286376953, 52.51518602243137],
    },
}


@pytest.fixture(params=["idea", "mapidea"])
def contact_form_factory(request, module, user, area_settings_factory):
    if request.param == "idea":

        def factory(data=None):
            return IdeaForm(data=data, module=module, user=user)

    else:
        area_settings_factory(module=module)

        def factory(data=None):
            data = dict(data or {})
            data.setdefault("point", POINT)
            return MapIdeaForm(
                data=data,
                module=module,
                user=user,
                settings_instance=module.settings_instance,
            )

    return factory


@pytest.mark.django_db
def test_contact_email_required_when_allow_contact(contact_form_factory):
    form = contact_form_factory(
        {
            "name": "Item",
            "description": "description",
            "allow_contact": True,
            "contact_email": "",
            "contact_storage_consent": True,
        }
    )
    assert not form.is_valid()
    assert "contact_email" in form.errors


@pytest.mark.django_db
def test_contact_consent_required_when_allow_contact(contact_form_factory, user):
    form = contact_form_factory(
        {
            "name": "Item",
            "description": "description",
            "allow_contact": True,
            "contact_email": user.email,
            "contact_storage_consent": False,
        }
    )
    assert not form.is_valid()
    assert "contact_storage_consent" in form.errors


@pytest.mark.django_db
def test_contact_optional_can_be_skipped(contact_form_factory):
    form = contact_form_factory(
        {"name": "Item", "description": "description", "allow_contact": False}
    )
    assert form.is_valid()
