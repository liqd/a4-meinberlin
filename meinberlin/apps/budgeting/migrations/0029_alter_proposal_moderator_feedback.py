# Generated by Django 3.2.16 on 2022-11-17 14:55

from django.db import migrations
import meinberlin.apps.moderatorfeedback.fields


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_budgeting", "0028_proposal_completed_tasks"),
    ]

    operations = [
        migrations.AlterField(
            model_name="proposal",
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
                verbose_name="Processing status (public)",
            ),
        ),
    ]
