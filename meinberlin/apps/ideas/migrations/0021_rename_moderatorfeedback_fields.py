# Generated by Django 3.2.16 on 2023-01-12 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_ideas", "0020_alter_idea_moderator_feedback"),
    ]

    operations = [
        migrations.RenameField(
            model_name="idea",
            old_name="moderator_statement",
            new_name="moderator_feedback_text",
        ),
        migrations.RenameField(
            model_name="idea",
            old_name="moderator_feedback",
            new_name="moderator_status",
        ),
    ]
