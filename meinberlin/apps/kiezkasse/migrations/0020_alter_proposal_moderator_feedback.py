# Generated by Django 3.2.16 on 2023-01-11 14:26

from django.db import migrations
import meinberlin.apps.moderatorfeedback.fields


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_kiezkasse", "0019_alter_proposal_moderator_feedback"),
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
                help_text="The status appears below the idea or proposal in red, yellow or green. The creator of the contribution receives a notification.",
                max_length=254,
                null=True,
                verbose_name="Status (public)",
            ),
        ),
    ]