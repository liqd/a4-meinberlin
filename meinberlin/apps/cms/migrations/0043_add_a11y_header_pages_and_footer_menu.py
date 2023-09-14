# Generated by Django 3.2.20 on 2023-09-26 15:29

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
        ("meinberlin_cms", "0042_upgrade_wagtail_image_related"),
    ]

    operations = [
        migrations.CreateModel(
            name="FooterMenuItem",
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
                ("column_title", models.CharField(max_length=255)),
                (
                    "page_link",
                    wagtail.fields.StreamField(
                        [
                            (
                                "link",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "link_text",
                                            wagtail.blocks.CharBlock(required=True),
                                        ),
                                        (
                                            "link",
                                            wagtail.blocks.PageChooserBlock(
                                                required=True
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "external_link",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "link_text",
                                            wagtail.blocks.CharBlock(required=True),
                                        ),
                                        (
                                            "link",
                                            wagtail.blocks.URLBlock(
                                                help_text="Please enter a full url which starts with https:// or http://",
                                                max_length=500,
                                                required=True,
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                        ],
                        use_json_field=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FooterNavigationMenu",
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
                ("title", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RenameModel(
            old_name="NavigationMenu",
            new_name="HeaderNavigationMenu",
        ),
        migrations.RenameModel(
            old_name="NavigationMenuItem",
            new_name="HeaderNavigationMenuItem",
        ),
        migrations.AddField(
            model_name="headerpages",
            name="accessibility_declaration",
            field=models.ForeignKey(
                blank=True,
                help_text="Please add a link to your accesibility decleration page.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="accessibility_declaration_page",
                to="wagtailcore.page",
                verbose_name="Accessibility Decleration Page",
            ),
        ),
        migrations.AddField(
            model_name="headerpages",
            name="accessibility_declaration_link_text",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="headerpages",
            name="additional_external_info",
            field=models.URLField(
                blank=True, help_text="Add link for additional information"
            ),
        ),
        migrations.AddField(
            model_name="headerpages",
            name="additional_external_info_link_text",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="headerpages",
            name="feedback_email",
            field=models.EmailField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="headerpages",
            name="feedback_name",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="headerpages",
            name="feedback_phone",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.CreateModel(
            name="FooterNavigationMenuItem",
            fields=[
                (
                    "footermenuitem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="meinberlin_cms.footermenuitem",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "parent",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="meinberlin_cms.footernavigationmenu",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
            bases=("meinberlin_cms.footermenuitem", models.Model),
        ),
    ]
