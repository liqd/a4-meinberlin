import pytest
from dateutil.parser import parse


@pytest.mark.django_db
def test_offline_event_item_save_updates_phase_dates(
    phase_factory, offline_event_item_factory
):
    """Test that saving an OfflineEventItem updates the phase start_date and end_date"""
    phase = phase_factory(module__blueprint_type="OE")
    module = phase.module

    # Create item with event_date
    event_date = parse("2023-06-15 14:30:00 UTC")
    offline_event_item_factory(module=module, event_date=event_date)

    # Phase dates should be updated to match event_date
    phase.refresh_from_db()
    assert phase.start_date == event_date
    assert phase.end_date == event_date


@pytest.mark.django_db
def test_offline_event_item_save_updates_module_name(
    phase_factory, offline_event_item_factory
):
    """Test that saving an OfflineEventItem with a name updates the module name"""
    phase = phase_factory(module__blueprint_type="OE")
    module = phase.module
    original_name = module.name

    # Create item with name
    offline_event_item_factory(module=module, name="Test Event Name")

    # Module name should be updated
    module.refresh_from_db()
    assert module.name == "Test Event Name"
    assert module.name != original_name


@pytest.mark.django_db
def test_offline_event_item_save_without_event_date(
    phase_factory, offline_event_item_factory
):
    """Test that saving without event_date doesn't update phase dates"""
    phase = phase_factory(module__blueprint_type="OE")
    module = phase.module
    original_start_date = phase.start_date
    original_end_date = phase.end_date

    # Create item without event_date
    offline_event_item_factory(module=module, event_date=None)

    # Phase dates should remain unchanged
    phase.refresh_from_db()
    assert phase.start_date == original_start_date
    assert phase.end_date == original_end_date


@pytest.mark.django_db
def test_offline_event_item_save_without_event_date_does_not_update_phase(
    phase_factory, offline_event_item_factory
):
    """Test that saving without event_date doesn't update phase dates even if module_id exists"""
    phase = phase_factory(module__blueprint_type="OE")
    module = phase.module
    original_start_date = phase.start_date
    original_end_date = phase.end_date

    # Create item with module but without event_date
    item = offline_event_item_factory(module=module, event_date=None)

    # Phase dates should remain unchanged because event_date is None
    phase.refresh_from_db()
    assert phase.start_date == original_start_date
    assert phase.end_date == original_end_date

    # Now set event_date and save - phase should be updated
    event_date = parse("2023-06-15 14:30:00 UTC")
    item.event_date = event_date
    item.save()

    # Phase dates should now be updated
    phase.refresh_from_db()
    assert phase.start_date == event_date
    assert phase.end_date == event_date
