# Generated by Django 3.2.20 on 2023-11-16 11:35

from bs4 import BeautifulSoup
from django.db import migrations


def replace_iframe_with_figur(apps, schema_editor):
    template = (
        '<figure class="media"><div data-oembed-url="{url}"><div><iframe src="'
        '{url}"></iframe></div></div></figure>'
    )
    OfflineEvent = apps.get_model("meinberlin_offlineevents", "OfflineEvent")
    for offline_event in OfflineEvent.objects.all():
        soup = BeautifulSoup(offline_event.description, "html.parser")
        iframes = soup.findAll("iframe")
        for iframe in iframes:
            figure = BeautifulSoup(
                template.format(url=iframe.attrs["src"]), "html.parser"
            )
            iframe.replaceWith(figure)
        if iframes:
            offline_event.description = soup.prettify(formatter="html")
            offline_event.save()


class Migration(migrations.Migration):
    dependencies = [
        ("meinberlin_offlineevents", "0010_alter_offlineevent_description"),
    ]

    operations = [
        migrations.RunPython(
            replace_iframe_with_figur,
        ),
    ]
