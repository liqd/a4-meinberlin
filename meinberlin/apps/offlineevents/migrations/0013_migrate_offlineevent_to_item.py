# by hand: migrate OfflineEvent to OfflineEventItem and create modules
from django.db import migrations, models


def migrate_events_to_items(apps, schema_editor):
    OfflineEvent = apps.get_model("meinberlin_offlineevents", "OfflineEvent")
    OfflineEventItem = apps.get_model("meinberlin_offlineevents", "OfflineEventItem")
    Module = apps.get_model("a4modules", "Module")
    Phase = apps.get_model("a4phases", "Phase")

    # Group events by project to assign sensible module weights
    events = list(OfflineEvent.objects.select_related("project").all())
    # Cache the next weight per project
    next_weight_by_project = {}

    for ev in events:
        project = ev.project
        # Determine the next weight per project (based on existing modules)
        if project.id not in next_weight_by_project:
            last = Module.objects.filter(project=project).order_by("-weight").first()
            next_weight_by_project[project.id] = (last.weight + 1) if last else 1

        # Create a module for this event
        # Prefer the event name, otherwise use a fallback
        module_name = ev.name or "Offline Event"
        module = Module.objects.create(
            name=module_name,
            project=project,
            weight=next_weight_by_project[project.id],
            is_draft=False,
            blueprint_type="OE",
        )
        next_weight_by_project[project.id] += 1

        # Create a phase (single-day event, start=end=ev.date)
        Phase.objects.create(
            name="Offline event phase",
            description=module.description or "",
            type="meinberlin_offlineevents:offline-event",
            module=module,
            start_date=ev.date,
            end_date=ev.date,
            weight=0,
        )

        # Create the item and transfer the fields
        OfflineEventItem.objects.create(
            module=module,
            creator=getattr(ev, "creator", None),
            name=ev.name,
            event_date=ev.date,
            event_type=ev.event_type,
            description=ev.description,
        )


def noop_reverse(apps, schema_editor):
    # No automatic reverse migration
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("meinberlin_offlineevents", "0012_offlineeventitem"),
        # ensure Item is already polymorph und polymorphic_ctype wurde für bestehende
        # Items befüllt, bevor wir neue OfflineEventItems erzeugen
        ("a4modules", "0010_populate_item_polymorphic_ctype"),
        ("a4phases", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offlineeventitem",
            name="name",
            field=models.CharField(
                blank=True, max_length=120, null=True, verbose_name="Name"
            ),
        ),
        migrations.RunPython(migrate_events_to_items, noop_reverse),
    ]
