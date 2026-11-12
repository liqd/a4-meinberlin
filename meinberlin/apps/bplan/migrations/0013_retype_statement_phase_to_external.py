from django.db import migrations

OLD_TYPE = "meinberlin_bplan:statement"
NEW_TYPE = "meinberlin_extprojects:external"


def retype_statement_phases(apps, schema_editor):
    """Bplans now reuse the Statement-free ExternalPhase to hold their
    participation dates, so re-type the legacy phase rows accordingly."""
    Phase = apps.get_model("a4phases", "Phase")
    Phase.objects.filter(type=OLD_TYPE).update(type=NEW_TYPE)


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_bplan", "0012_remove_bplan_identifier"),
        ("a4phases", "0007_order_phases_also_by_id"),
    ]

    operations = [
        # Not reversible: once re-typed we cannot distinguish Bplan phases from
        # genuine external-project phases, so the reverse is a no-op.
        migrations.RunPython(retype_statement_phases, migrations.RunPython.noop),
    ]
