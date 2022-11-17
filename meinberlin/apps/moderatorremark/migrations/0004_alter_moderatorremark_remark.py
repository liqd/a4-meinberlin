# Generated by Django 3.2.16 on 2022-11-17 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_moderatorremark', '0003_use_textfield'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderatorremark',
            name='remark',
            field=models.TextField(blank=True, help_text='Here you can write a moderation remark. It is only displayed for moderators and initiators of your project.', verbose_name='Moderation remark (internal)'),
        ),
    ]
