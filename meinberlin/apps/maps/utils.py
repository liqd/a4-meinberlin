from adhocracy4.maps_react.utils import get_map_settings


def get_selected_map_layer(module):
    """Return the active GDI WMS layer as map settings data."""
    layer = module.map_layers.filter(is_active=True).first()
    if not layer:
        return None
    return {
        "url": layer.service_url,
        "layers": layer.layer_name,
        "title": layer.name,
        "attribution": layer.attribution or "GDI Berlin",
    }


def get_map_settings_with_layer(module, **kwargs):
    """Return map settings, adding the selected GDI layer when available."""
    layer = get_selected_map_layer(module)
    if layer:
        kwargs["layer"] = layer
    return get_map_settings(**kwargs)
