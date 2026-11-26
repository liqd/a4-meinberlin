import re
from urllib.parse import urlsplit
from xml.etree.ElementTree import ParseError

import requests
from defusedxml import ElementTree
from defusedxml.common import DefusedXmlException
from django.core.cache import cache
from django.utils.translation import gettext as _

GDI_HOST = "gdi.berlin.de"
WMS_PATH_PREFIX = "/services/wms/"
CAPABILITIES_CACHE_TIMEOUT = 60 * 60 * 24
REQUEST_TIMEOUT = 10
MAX_RESPONSE_SIZE = 2 * 1024 * 1024
SERVICE_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class MapLayerError(Exception):
    """A user-facing error while resolving a GDI WMS layer."""

    def __init__(self, message, code="unusable"):
        super().__init__(message)
        self.message = message
        self.code = code


def parse_service_id(raw_url):
    """Return the GDI WMS service id from a supported service URL.

    Only links to the GDI Berlin WMS service endpoints are accepted. Query
    strings and fragments are ignored so that capabilities URLs, links copied
    from the viewer, and bare service links all resolve to the same service.
    """
    if not isinstance(raw_url, str) or not raw_url.strip():
        raise MapLayerError(
            _("Please enter a link to a map service from the Berlin geoportal."),
            "invalid_url",
        )

    url = urlsplit(raw_url.strip())
    if url.scheme != "https" or (url.hostname or "").lower() != GDI_HOST:
        raise MapLayerError(
            _("Only links from gdi.berlin.de are allowed."),
            "invalid_host",
        )
    try:
        has_port = bool(url.port)
    except ValueError:
        has_port = True
    if url.username or url.password or has_port:
        raise MapLayerError(
            _("Only links from gdi.berlin.de are allowed."),
            "invalid_host",
        )

    path = url.path.rstrip("/")
    if not path.startswith(WMS_PATH_PREFIX):
        raise MapLayerError(
            _("Please enter a link to a WMS map service from the Berlin geoportal."),
            "invalid_path",
        )

    service_id = path[len(WMS_PATH_PREFIX) :]
    if not service_id or "/" in service_id or not SERVICE_ID_PATTERN.match(service_id):
        raise MapLayerError(
            _("Please enter a link to a WMS map service from the Berlin geoportal."),
            "invalid_path",
        )

    return service_id


def service_url(service_id):
    return f"https://{GDI_HOST}{WMS_PATH_PREFIX}{service_id}"


def capabilities_url(service_id):
    return (
        f"{service_url(service_id)}?service=WMS&request=GetCapabilities&version=1.3.0"
    )


def resolve_map_layer_url(raw_url):
    """Resolve a pasted GDI service URL to its WMS service and layers."""
    service_id = parse_service_id(raw_url)
    return get_service_layers(service_id)


def get_service_layers(service_id):
    cache_key = f"gdi_wms_capabilities_{service_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    root = _fetch_capabilities(service_id)
    service = _child(root, "Service")
    capability = _child(root, "Capability")
    get_map = _child(_child(capability, "Request"), "GetMap")
    root_layer = _child(capability, "Layer")
    if None in (service, capability, get_map, root_layer):
        raise MapLayerError(
            _("The link does not lead to a usable map layer."),
            "unusable",
        )

    service_title = _text(service, "Title") or service_id
    default_attribution = (
        _text(root_layer, "Attribution/Title")
        or _text(service, "Title")
        or "GDI Berlin"
    )
    layers = _collect_layers(root_layer, default_attribution)
    if not layers:
        raise MapLayerError(
            _("The link does not lead to a usable map layer."),
            "no_layers",
        )

    result = {
        "service_id": service_id,
        "service_url": service_url(service_id),
        "service_title": service_title,
        "version": root.attrib.get("version") or "1.3.0",
        "format": _image_format(get_map),
        "layers": layers,
    }
    cache.set(cache_key, result, CAPABILITIES_CACHE_TIMEOUT)
    return result


def _fetch_capabilities(service_id):
    """Fetch and sanity check the capabilities document of a GDI service."""
    try:
        response = requests.get(
            capabilities_url(service_id),
            timeout=REQUEST_TIMEOUT,
            allow_redirects=False,
        )
    except requests.RequestException:
        raise MapLayerError(
            _("The map service could not be reached. Please try again later."),
            "unreachable",
        )

    if response.status_code != 200:
        raise MapLayerError(
            _("The map service could not be reached. Please try again later."),
            "unreachable",
        )
    if len(response.content) > MAX_RESPONSE_SIZE:
        raise MapLayerError(
            _("The link does not lead to a usable map layer."),
            "unusable",
        )

    try:
        root = ElementTree.fromstring(response.content)
    except (ParseError, DefusedXmlException, ValueError):
        raise MapLayerError(
            _("The link does not lead to a usable map layer."),
            "unusable",
        )

    if _local_name(root.tag) not in {"WMS_Capabilities", "WMT_MS_Capabilities"}:
        raise MapLayerError(
            _("The link does not lead to a usable map layer."),
            "unusable",
        )

    return root


def _image_format(get_map):
    formats = [
        _element_text(format_el)
        for format_el in _children(get_map, "Format")
        if _element_text(format_el)
    ]
    if not formats or "image/png" in formats:
        return "image/png"
    return next(
        (value for value in formats if value.startswith("image/")),
        "image/png",
    )


def _collect_layers(root_layer, inherited_attribution):
    leaf_layers = []
    named_layers = []

    def walk(layer_el):
        name = _text(layer_el, "Name")
        child_layers = _children(layer_el, "Layer")
        has_named_children = any(_text(child, "Name") for child in child_layers)

        if name:
            layer = {
                "name": name,
                "title": _text(layer_el, "Title") or name,
                "abstract": _text(layer_el, "Abstract"),
                "attribution": _text(layer_el, "Attribution/Title")
                or inherited_attribution,
                "legend_url": _legend_url(layer_el),
            }
            named_layers.append(layer)
            if not has_named_children:
                leaf_layers.append(layer)

        for child in child_layers:
            walk(child)

    for child in _children(root_layer, "Layer"):
        walk(child)

    return leaf_layers or named_layers


def _legend_url(layer_el):
    for style in _children(layer_el, "Style"):
        legend = _child(style, "LegendURL")
        if legend is None:
            continue
        online_resource = _child(legend, "OnlineResource")
        if online_resource is not None:
            return _href(online_resource)
    return ""


def _href(element):
    return (
        element.attrib.get("{http://www.w3.org/1999/xlink}href")
        or element.attrib.get("href")
        or ""
    )


def _local_name(tag):
    return str(tag).rsplit("}", 1)[-1]


def _child(element, name):
    if element is None:
        return None
    for child in element:
        if _local_name(child.tag) == name:
            return child
    return None


def _children(element, name):
    if element is None:
        return []
    return [child for child in element if _local_name(child.tag) == name]


def _element_text(element):
    if element is None:
        return ""
    return "".join(element.itertext()).strip()


def _text(element, path):
    if element is None:
        return ""
    if not path:
        return _element_text(element)
    current = element
    for part in path.split("/"):
        current = _child(current, part)
        if current is None:
            return ""
    return _element_text(current)
