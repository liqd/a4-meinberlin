# Generated by Django 4.2 on 2023-11-29 10:08

from django.conf import settings
from django.db import migrations


def add_topics(apps, schema_editor):
    if hasattr(settings, "A4_PROJECT_TOPICS"):
        Topic = apps.get_model("a4projects", "Topic")
        for topic in settings.A4_PROJECT_TOPICS:
            Topic.objects.get_or_create(code=topic[0], name=topic[1])


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("meinberlin_projects", "0004_verbose_name_created_modified"),
    ]

    operations = [
        migrations.RunPython(add_topics, reverse_func),
    ]
