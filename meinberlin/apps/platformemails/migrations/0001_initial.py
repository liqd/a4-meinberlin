# Generated by Django 2.2.12 on 2020-05-14 13:48

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PlatformEmail",
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
                (
                    "created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(blank=True, editable=False, null=True),
                ),
                ("sender_name", models.CharField(max_length=254, verbose_name="Name")),
                (
                    "sender",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="Sender"
                    ),
                ),
                ("subject", models.CharField(max_length=254, verbose_name="Subject")),
                (
                    "body",
                    models.TextField(blank=True, verbose_name="Email body"),
                ),
                (
                    "sent",
                    models.DateTimeField(blank=True, null=True, verbose_name="Sent"),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
