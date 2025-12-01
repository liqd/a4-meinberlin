from django.db import migrations


def fix_offlineeventitem_polymorphic_ctype(apps, schema_editor):
    """Backfill polymorphic_ctype for existing OfflineEventItem rows."""

    OfflineEventItem = apps.get_model("meinberlin_offlineevents", "OfflineEventItem")
    ContentType = apps.get_model("contenttypes", "ContentType")

    db_alias = schema_editor.connection.alias

    # Determine ContentType for OfflineEventItem (for polymorphic relation)
    ct = ContentType.objects.db_manager(db_alias).get_for_model(
        OfflineEventItem, for_concrete_model=False
    )

    # Only update rows where polymorphic_ctype is not set yet
    (
        OfflineEventItem.objects.using(db_alias)
        .filter(polymorphic_ctype__isnull=True)
        .update(polymorphic_ctype=ct)
    )


def delete_old_offlineevents(apps, schema_editor):
    """Delete legacy OfflineEvent rows that are no longer used as modules/items."""

    OfflineEvent = apps.get_model("meinberlin_offlineevents", "OfflineEvent")
    OfflineEventItem = apps.get_model("meinberlin_offlineevents", "OfflineEventItem")
    Module = apps.get_model("a4modules", "Module")

    db_alias = schema_editor.connection.alias

    offlineevents = OfflineEvent.objects.using(db_alias).select_related("project").all()

    for ev in offlineevents:
        # Get all modules of the project (from a4modules)
        project_modules = Module.objects.using(db_alias).filter(project=ev.project)

        # Check if there is an OfflineEventItem with matching date on any of these modules
        exists_matching_item = (
            OfflineEventItem.objects.using(db_alias)
            .filter(
                module__in=project_modules,
                event_date=ev.date,
            )
            .exists()
        )

        if exists_matching_item:
            ev.delete(using=db_alias)


def noop_reverse(apps, schema_editor):
    # No automatic reverse migration needed
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_offlineevents", "0015_alter_offlineeventitem_name"),
    ]

    operations = [
        migrations.RunPython(
            fix_offlineeventitem_polymorphic_ctype,
            reverse_code=noop_reverse,
        ),
        migrations.RunPython(
            delete_old_offlineevents,
            reverse_code=noop_reverse,
        ),
    ]
