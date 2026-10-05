import pytest

from meinberlin.apps.ideas.forms import IdeaForm
from meinberlin.apps.mapideas.forms import MapIdeaForm
from meinberlin.test.helpers import GuestUserCreator

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

        def factory(data=None, form_user=user):
            return IdeaForm(data=data, module=module, user=form_user)

    else:
        area_settings_factory(module=module)

        def factory(data=None, form_user=user):
            data = dict(data or {})
            data.setdefault("point", POINT)
            return MapIdeaForm(
                data=data,
                module=module,
                user=form_user,
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


@pytest.mark.django_db
def test_guest_contact_fields_hidden(contact_form_factory):
    guest = GuestUserCreator().create_guest_user()
    form = contact_form_factory(form_user=guest)

    assert form.show_contact_info is False
    for field in (
        "allow_contact",
        "contact_email",
        "contact_phone",
        "contact_storage_consent",
    ):
        assert field not in form.fields


@pytest.mark.django_db
def test_guest_can_submit_without_contact(contact_form_factory):
    guest = GuestUserCreator().create_guest_user()
    form = contact_form_factory(
        {"name": "Item", "description": "description"}, form_user=guest
    )

    assert form.is_valid()
    instance = form.save(commit=False)
    assert instance.allow_contact is False
    assert instance.contact_email == ""
    assert instance.contact_phone == ""


@pytest.mark.django_db
def test_guest_posted_contact_is_ignored(contact_form_factory):
    guest = GuestUserCreator().create_guest_user()
    form = contact_form_factory(
        {
            "name": "Item",
            "description": "description",
            "allow_contact": True,
            "contact_email": "guest-contact@example.com",
            "contact_phone": "0123456789",
            "contact_storage_consent": True,
        },
        form_user=guest,
    )

    assert form.is_valid()
    instance = form.save(commit=False)
    assert instance.allow_contact is False
    assert instance.contact_email == ""
    assert instance.contact_phone == ""
