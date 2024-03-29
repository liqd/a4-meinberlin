# Generated by Django 2.2.19 on 2021-03-24 15:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_users", "0006_regform_notification_checkbox"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                error_messages={
                    "unique": "A user with that username already exists.",
                    "used_as_email": "This username is already used as an e-mail address.",
                },
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
