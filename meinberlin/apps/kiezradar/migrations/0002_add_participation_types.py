from django.db import migrations


def populate_project_type(apps, schema_editor):
    ProjectType = apps.get_model("meinberlin_kiezradar", "ProjectType")
    ProjectType.objects.bulk_create(
        [
            ProjectType(participation=0),
            ProjectType(participation=1),
            ProjectType(participation=2),
            ProjectType(participation=3),
        ]
    )


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_kiezradar", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_project_type),
    ]
