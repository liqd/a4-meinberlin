import pytest
from django.urls import reverse

from adhocracy4.dashboard import components

component_module = components.modules.get("module_offlineevent")
component_settings = components.modules.get("offlineevent_settings")


@pytest.mark.django_db
def test_module_component_is_effective(module_factory):
    module_oe = module_factory(blueprint_type="OE")
    module_ic = module_factory(blueprint_type="IC")

    assert component_module.is_effective(module_oe) is True
    assert component_module.is_effective(module_ic) is False


@pytest.mark.django_db
def test_module_component_progress(phase_factory, offline_event_item_factory):
    phase = phase_factory(module__blueprint_type="OE")
    module = phase.module

    # No item exists
    assert component_module.get_progress(module) == (0, 3)

    # Item with no fields filled
    item = offline_event_item_factory(
        module=module, name="", event_type="", description="", event_date=None
    )
    assert component_module.get_progress(module) == (0, 3)

    # Item with one field filled
    item.name = "Test Event"
    item.save()
    assert component_module.get_progress(module) == (1, 3)

    # Item with two fields filled
    item.event_type = "Workshop"
    item.save()
    assert component_module.get_progress(module) == (2, 3)

    # Item with all fields filled
    item.description = "Test description"
    item.save()
    assert component_module.get_progress(module) == (3, 3)


@pytest.mark.django_db
def test_module_component_base_url(module_factory):
    module = module_factory(blueprint_type="OE")
    assert component_module.get_base_url(module) == reverse(
        "a4dashboard:offlineevent-module", kwargs={"module_slug": module.slug}
    )


@pytest.mark.django_db
def test_settings_component_is_effective(module_factory):
    module_oe = module_factory(blueprint_type="OE")
    module_ic = module_factory(blueprint_type="IC")

    assert component_settings.is_effective(module_oe) is True
    assert component_settings.is_effective(module_ic) is False


@pytest.mark.django_db
def test_settings_component_progress(phase_factory, offline_event_item_factory):
    phase = phase_factory(module__blueprint_type="OE")
    module = phase.module

    # No item exists
    assert component_settings.get_progress(module) == (0, 1)

    # Item without event_date
    item = offline_event_item_factory(module=module, event_date=None)
    assert component_settings.get_progress(module) == (0, 1)

    # Item with event_date
    from dateutil.parser import parse

    item.event_date = parse("2023-01-15 14:30:00 UTC")
    item.save()
    assert component_settings.get_progress(module) == (1, 1)


@pytest.mark.django_db
def test_settings_component_base_url(module_factory):
    module = module_factory(blueprint_type="OE")
    assert component_settings.get_base_url(module) == reverse(
        "a4dashboard:offlineevent-settings", kwargs={"module_slug": module.slug}
    )
