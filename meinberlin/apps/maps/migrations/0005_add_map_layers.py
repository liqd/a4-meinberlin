from django.db import migrations

MAP_LAYERS = [
    {
        "slug": "fnp-2025",
        "name": "Flächennutzungsplan Berlin 2025",
        "url": "https://gdi.berlin.de/services/wms/fnp_2025",
        "layer_name": "fnp_2025",
        "attribution": (
            "© GDI Berlin / Senatsverwaltung für Stadtentwicklung, Bauen und "
            "Wohnen | Datenlizenz Deutschland – Zero – 2.0"
        ),
        "opacity": 0.7,
        "order": 10,
    },
    {
        "slug": "umweltatlas-flaechennutzung-2020",
        "name": "Flächennutzung 2020 (Umweltatlas)",
        "url": "https://gdi.berlin.de/services/wms/ua_flaechennutzung_2020",
        "layer_name": "c_ua_realnutz_2020",
        "attribution": (
            "© GDI Berlin / Senatsverwaltung für Stadtentwicklung, Bauen und "
            "Wohnen | Datenlizenz Deutschland – Zero – 2.0"
        ),
        "opacity": 0.7,
        "order": 20,
    },
    {
        "slug": "dop-2021",
        "name": "Digitale Orthophotos 2021",
        "url": "https://gdi.berlin.de/services/wms/dop_2021",
        "layer_name": "dop_2021_rgb",
        "attribution": (
            "© GDI Berlin / Senatsverwaltung für Stadtentwicklung, Bauen und "
            "Wohnen | Datenlizenz Deutschland – Zero – 2.0"
        ),
        "opacity": 0.7,
        "order": 30,
    },
]


def add_map_layers(apps, schema_editor):
    MapLayer = apps.get_model("meinberlin_maps", "MapLayer")
    for layer in MAP_LAYERS:
        slug = layer["slug"]
        defaults = {key: value for key, value in layer.items() if key != "slug"}
        MapLayer.objects.update_or_create(slug=slug, defaults=defaults)


def remove_map_layers(apps, schema_editor):
    MapLayer = apps.get_model("meinberlin_maps", "MapLayer")
    MapLayer.objects.filter(slug__in=[layer["slug"] for layer in MAP_LAYERS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_maps", "0004_maplayer_modulemaplayer"),
    ]

    operations = [
        migrations.RunPython(add_map_layers, remove_map_layers),
    ]
