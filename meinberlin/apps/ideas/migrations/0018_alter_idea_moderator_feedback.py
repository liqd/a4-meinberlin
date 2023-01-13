# Generated by Django 3.2.16 on 2022-11-11 10:43

from django.db import migrations
import meinberlin.apps.moderatorfeedback.fields


def moderator_feedback_checked_to_qualified(apps, schema_editor):
    Idea = apps.get_model("meinberlin_ideas", "Idea")

    for idea in Idea.objects.filter(moderator_feedback="CHECKED"):
        idea.moderator_feedback = "QUALIFIED"
        idea.save()


def moderator_feedback_qualified_to_checked(apps, schema_editor):
    Idea = apps.get_model("meinberlin_ideas", "Idea")

    for idea in Idea.objects.filter(moderator_feedback="QUALIFIED"):
        idea.moderator_feedback = "CHECKED"
        idea.save()


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_ideas", "0017_alter_idea_moderator_feedback"),
    ]

    operations = [
        migrations.AlterField(
            model_name="idea",
            name="moderator_feedback",
            field=meinberlin.apps.moderatorfeedback.fields.ModeratorFeedbackField(
                blank=True,
                choices=[
                    ("CONSIDERATION", "Under consideration"),
                    ("QUALIFIED", "Qualified for next phase"),
                    ("REJECTED", "Rejected"),
                    ("ACCEPTED", "Accepted"),
                ],
                default=None,
                help_text="The editing status appears below the title of the idea in red, yellow or green. The idea provider receives a notification.",
                max_length=254,
                null=True,
                verbose_name="Processing status",
            ),
        ),
        migrations.RunPython(
            moderator_feedback_checked_to_qualified,
            moderator_feedback_qualified_to_checked,
        ),
    ]
