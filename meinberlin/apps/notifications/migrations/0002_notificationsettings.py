# Generated by Django 4.2.16 on 2025-02-19 06:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("meinberlin_notifications", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="NotificationSettings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email_newsletter", models.BooleanField(default=False)),
                ("notify_followers_phase_started", models.BooleanField(default=True)),
                ("notify_followers_phase_over_soon", models.BooleanField(default=True)),
                ("notify_followers_event_upcoming", models.BooleanField(default=True)),
                ("notify_creator", models.BooleanField(default=True)),
                (
                    "notify_creator_on_moderator_feedback",
                    models.BooleanField(default=True),
                ),
                (
                    "notify_initiators_project_created",
                    models.BooleanField(default=True),
                ),
                ("notify_moderator", models.BooleanField(default=True)),
                ("track_followers_phase_started", models.BooleanField(default=True)),
                ("track_followers_phase_over_soon", models.BooleanField(default=True)),
                ("track_followers_event_upcoming", models.BooleanField(default=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notification_settings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
