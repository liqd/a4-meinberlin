from textwrap import dedent

import pytest
from django.core.cache import cache

from meinberlin.apps.maps import gdi_wms


@pytest.fixture(autouse=True)
def clear_capabilities_cache():
    cache.clear()
    yield
    cache.clear()


def wms_capabilities(layers):
    layer_xml = "".join(f"""
        <Layer>
          <Name>{name}</Name>
          <Title>{title}</Title>
          <Abstract>{title} abstract</Abstract>
        </Layer>
        """ for name, title in layers)
    return dedent(f"""\
        <?xml version="1.0" encoding="UTF-8"?>
        <WMS_Capabilities
            xmlns="http://www.opengis.net/wms"
            version="1.3.0">
          <Service>
            <Name>WMS</Name>
            <Title>Baumbestand Berlin</Title>
          </Service>
          <Capability>
            <Request>
              <GetMap>
                <Format>image/png</Format>
              </GetMap>
            </Request>
            <Layer>
              {layer_xml}
            </Layer>
          </Capability>
        </WMS_Capabilities>
        """)


@pytest.mark.parametrize(
    "url",
    [
        "https://gdi.berlin.de/services/wms/baumbestand",
        "https://gdi.berlin.de/services/wms/baumbestand/",
        "https://gdi.berlin.de/services/wms/baumbestand?request=GetCapabilities&service=WMS",
    ],
)
def test_parse_service_id_accepts_service_links(url):
    assert gdi_wms.parse_service_id(url) == "baumbestand"


@pytest.mark.parametrize(
    "url",
    [
        "http://gdi.berlin.de/services/wms/baumbestand",
        "https://example.com/services/wms/baumbestand",
        "https://gdi.berlin.de/services/wfs/baumbestand",
        "https://gdi.berlin.de/view/baumbestand",
        "https://gdi.berlin.de/services/wms/baumbestand/extra",
    ],
)
def test_parse_service_id_rejects_other_links(url):
    with pytest.raises(gdi_wms.MapLayerError):
        gdi_wms.parse_service_id(url)


def test_resolve_single_layer_service(requests_mock):
    requests_mock.get(
        gdi_wms.capabilities_url("baumbestand_gruen_berlin"),
        text=wms_capabilities([("anlagenbaum_gruenberlin", "Baumbestand Grün Berlin")]),
    )

    result = gdi_wms.resolve_map_layer_url(
        "https://gdi.berlin.de/services/wms/baumbestand_gruen_berlin"
    )

    assert result["service_url"] == (
        "https://gdi.berlin.de/services/wms/baumbestand_gruen_berlin"
    )
    assert result["service_title"] == "Baumbestand Berlin"
    assert result["layers"] == [
        {
            "name": "anlagenbaum_gruenberlin",
            "title": "Baumbestand Grün Berlin",
            "abstract": "Baumbestand Grün Berlin abstract",
            "attribution": "Baumbestand Berlin",
            "legend_url": "",
        }
    ]


def test_resolve_multi_layer_service(requests_mock):
    requests_mock.get(
        gdi_wms.capabilities_url("baumbestand"),
        text=wms_capabilities(
            [
                ("anlagenbaeume", "Anlagenbäume"),
                ("strassenbaeume", "Straßenbäume"),
            ]
        ),
    )

    result = gdi_wms.resolve_map_layer_url(
        "https://gdi.berlin.de/services/wms/baumbestand"
    )

    assert [layer["name"] for layer in result["layers"]] == [
        "anlagenbaeume",
        "strassenbaeume",
    ]


def test_resolve_rejects_non_wms_response(requests_mock):
    requests_mock.get(
        gdi_wms.capabilities_url("baumbestand"),
        text="<html>not a WMS</html>",
    )

    with pytest.raises(gdi_wms.MapLayerError) as error:
        gdi_wms.resolve_map_layer_url("https://gdi.berlin.de/services/wms/baumbestand")

    assert error.value.code == "unusable"


def test_resolve_rejects_unreachable_service(requests_mock):
    requests_mock.get(
        gdi_wms.capabilities_url("baumbestand"),
        status_code=503,
    )

    with pytest.raises(gdi_wms.MapLayerError) as error:
        gdi_wms.resolve_map_layer_url("https://gdi.berlin.de/services/wms/baumbestand")

    assert error.value.code == "unreachable"


def test_capabilities_are_cached(requests_mock):
    adapter = requests_mock.get(
        gdi_wms.capabilities_url("baumbestand"),
        text=wms_capabilities([("strassenbaeume", "Straßenbäume")]),
    )

    gdi_wms.get_service_layers("baumbestand")
    gdi_wms.get_service_layers("baumbestand")

    assert adapter.call_count == 1
