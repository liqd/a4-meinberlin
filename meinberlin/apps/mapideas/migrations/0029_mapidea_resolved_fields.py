from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_mapideas", "0028_mapidea_is_reviewed"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    "ALTER TABLE meinberlin_mapideas_mapidea ADD COLUMN "
                    "is_resolved boolean NOT NULL DEFAULT FALSE;",
                    reverse_sql="ALTER TABLE meinberlin_mapideas_mapidea DROP COLUMN is_resolved;",
                ),
                migrations.RunSQL(
                    "ALTER TABLE meinberlin_mapideas_mapidea ADD COLUMN "
                    "resolved_at timestamp with time zone NULL;",
                    reverse_sql="ALTER TABLE meinberlin_mapideas_mapidea DROP COLUMN resolved_at;",
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="mapidea",
                    name="is_resolved",
                    field=models.BooleanField(default=False),
                ),
                migrations.AddField(
                    model_name="mapidea",
                    name="resolved_at",
                    field=models.DateTimeField(blank=True, null=True),
                ),
            ],
        ),
    ]
