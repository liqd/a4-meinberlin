# Generated by Django 3.2.16 on 2023-01-12 11:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "meinberlin_moderatorfeedback",
            "0005_rename_statement_moderatorstatement_feedback_text",
        ),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ModeratorStatement",
            new_name="ModeratorFeedback",
        ),
    ]
