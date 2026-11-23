import json
from unittest.mock import patch

import pytest
from django.urls import reverse

from meinberlin.apps.maps import gdi_wms


@pytest.fixture
def resolve_url(module):
    return reverse("a4dashboard:map-layer-resolve", kwargs={"module_slug": module.slug})


@pytest.fixture
def initiator_client(client, module):
    initiator = module.project.organisation.initiators.first()
    client.login(username=initiator.email, password="password")
    return client


def post_json(client, url, payload):
    return client.post(url, data=json.dumps(payload), content_type="application/json")


def service_payload():
    return {
        "service_id": "baumbestand",
        "service_url": "https://gdi.berlin.de/services/wms/baumbestand",
        "service_title": "Baumbestand Berlin",
        "version": "1.3.0",
        "format": "image/png",
        "layers": [
            {
                "name": "anlagenbaeume",
                "title": "Anlagenbäume",
                "abstract": "",
                "attribution": "GDI Berlin",
                "legend_url": "",
            },
            {
                "name": "strassenbaeume",
                "title": "Straßenbäume",
                "abstract": "",
                "attribution": "GDI Berlin",
                "legend_url": "",
            },
        ],
    }


@pytest.mark.django_db
def test_requires_permission(client, module, resolve_url, user):
    client.login(username=user.email, password="password")
    response = post_json(
        client,
        resolve_url,
        {"url": "https://gdi.berlin.de/services/wms/baumbestand"},
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_anonymous_is_redirected_or_denied(client, resolve_url):
    response = post_json(
        client,
        resolve_url,
        {"url": "https://gdi.berlin.de/services/wms/baumbestand"},
    )
    assert response.status_code in (302, 403)


@pytest.mark.django_db
def test_rejects_foreign_host(initiator_client, resolve_url):
    response = post_json(
        initiator_client,
        resolve_url,
        {"url": "https://example.com/services/wms/baumbestand"},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["ok"] is False
    assert data["code"] == "invalid_host"


@pytest.mark.django_db
def test_rejects_non_wms_path(initiator_client, resolve_url):
    response = post_json(
        initiator_client,
        resolve_url,
        {"url": "https://gdi.berlin.de/services/wfs/baumbestand"},
    )
    assert response.status_code == 400
    assert response.json()["code"] == "invalid_path"


@pytest.mark.django_db
def test_rejects_unreadable_body(initiator_client, resolve_url):
    response = initiator_client.post(
        resolve_url, data="{not json", content_type="application/json"
    )
    assert response.status_code == 400
    assert response.json()["code"] == "invalid_request"


@pytest.mark.django_db
def test_returns_layers_for_valid_service(initiator_client, resolve_url):
    with patch(
        "meinberlin.apps.maps.gdi_wms.get_service_layers",
        return_value=service_payload(),
    ):
        response = post_json(
            initiator_client,
            resolve_url,
            {"url": "https://gdi.berlin.de/services/wms/baumbestand"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["service_url"] == "https://gdi.berlin.de/services/wms/baumbestand"
    assert data["service_title"] == "Baumbestand Berlin"
    assert data["format"] == "image/png"
    assert [layer["name"] for layer in data["layers"]] == [
        "anlagenbaeume",
        "strassenbaeume",
    ]


@pytest.mark.django_db
def test_reports_unreachable_service(initiator_client, resolve_url):
    with patch(
        "meinberlin.apps.maps.gdi_wms.get_service_layers",
        side_effect=gdi_wms.MapLayerError(
            "The map service could not be reached.", "unreachable"
        ),
    ):
        response = post_json(
            initiator_client,
            resolve_url,
            {"url": "https://gdi.berlin.de/services/wms/baumbestand"},
        )
    assert response.status_code == 400
    assert response.json()["code"] == "unreachable"
