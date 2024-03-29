# Generated by Django 2.2.6 on 2019-11-04 12:01

from django.db import migrations

from meinberlin.apps.extprojects.models import ExternalProject


def add_project_type(apps, schema_editor):
    objs = ExternalProject.objects.all()
    for obj in objs:
        obj.project_type = "meinberlin_extprojects.ExternalProject"
    ExternalProject.objects.bulk_update(objs, ["project_type"])


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_extprojects", "0004_add_start_and_end_date"),
        ("meinberlin_projects", "0002_custom_project_types"),
    ]

    operations = [migrations.RunPython(add_project_type)]
