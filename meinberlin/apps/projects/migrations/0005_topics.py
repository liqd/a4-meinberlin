# Generated by Django 4.2 on 2023-11-29 10:08

from django.db import migrations

A4_PROJECT_TOPICS = (
    ("ANT", "Anti-discrimination"),
    ("WOR", "Work & economy"),
    ("BUI", "Building & living"),
    ("EDU", "Education & research"),
    ("CHI", "Children, youth & family"),
    ("FIN", "Finances"),
    ("HEA", "Health & sports"),
    ("INT", "Integration"),
    ("CUL", "Culture & leisure"),
    ("NEI", "Neighborhood & participation"),
    ("URB", "Urban development"),
    ("ENV", "Environment & public green space"),
    ("TRA", "Traffic"),
)


def add_topics(apps, schema_editor):
    Topic = apps.get_model("a4projects", "Topic")
    for topic in A4_PROJECT_TOPICS:
        Topic(code=topic[0], name=topic[1]).save()


class Migration(migrations.Migration):
    dependencies = [
        ("meinberlin_projects", "0004_verbose_name_created_modified"),
    ]

    operations = [
        migrations.RunPython(
            add_topics,
        ),
    ]
