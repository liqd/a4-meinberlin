# Generated by Django 2.2.5 on 2019-09-04 13:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_users", "0005_default_user_newsletter_is_false"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="get_newsletters",
            field=models.BooleanField(
                default=False,
                help_text="Yes, I would like to receive e-mail newsletters about the projects I am following.",
                verbose_name="Newsletter",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="get_notifications",
            field=models.BooleanField(
                default=True,
                help_text="Yes, I would like to be notified by e-mail about the start and end of participation opportunities. This applies to all projects I follow. I also receive an e-mail when someone comments on one of my contributions.",
                verbose_name="Notifications",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                error_messages={"unique": "A user with that username already exists."},
                help_text="Your username will appear publicly next to your posts.",
                max_length=60,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[\\w]+[ \\w.@+-]*$",
                        "Enter a valid username. This value may contain only letters, digits, spaces and @/./+/-/_ characters. It must start with a digit or a letter.",
                        "invalid",
                    )
                ],
                verbose_name="username",
            ),
        ),
    ]
