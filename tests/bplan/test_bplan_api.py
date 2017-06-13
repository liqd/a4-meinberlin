import pytest
from dateutil.parser import parse
from django.core.urlresolvers import reverse
from rest_framework import status

from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from apps.bplan import models as bplan_models


@pytest.mark.django_db
def test_anonymous_cannot_add_bplan(apiclient, organisation):
    url = reverse('bplan-list', kwargs={'organisation_pk': organisation.pk})
    data = {}
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_non_initiator_cannot_add_bplan(apiclient, organisation, user):
    url = reverse('bplan-list', kwargs={'organisation_pk': organisation.pk})
    data = {}
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_initiator_add_bplan(apiclient, organisation):
    url = reverse('bplan-list', kwargs={'organisation_pk': organisation.pk})
    data = {
        "name": "bplan-1",
        "description": "desc",
        "url": "https://bplan.net",
        "office_worker_email": "test@liqd.de",
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
    }
    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    bplan = bplan_models.Bplan.objects.first()
    assert bplan.name == data['name']
    assert bplan.description == data['description']
    assert bplan.url == data['url']
    assert bplan.office_worker_email == data['office_worker_email']
    assert bplan.is_archived is False
    assert bplan.is_draft is False
    assert bplan.information == ''
    assert bplan.result == ''
    module = module_models.Module.objects.get(project=bplan)
    assert module is not None
    phase = phase_models.Phase.objects.get(module=module)
    assert phase is not None
    assert phase.start_date == parse("2013-01-01 17:00:00 UTC")
    assert phase.end_date == parse("2021-01-01 17:00:00 UTC")


@pytest.mark.django_db
def test_initiator_update_bplan(apiclient, bplan, phase):
    phase.module.project = bplan
    phase.module.save()
    url = reverse(
        'bplan-detail',
        kwargs={
            'organisation_pk': bplan.organisation.pk,
            'pk': bplan.pk
        }
    )
    data = {
        "name": "bplan-1",
        "description": "desc",
        "url": "https://bplan.net",
        "office_worker_email": "test@liqd.de",
        "is_draft": "true",
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
    }
    user = bplan.organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    bplan = bplan_models.Bplan.objects.first()
    assert bplan.is_draft is True


@pytest.mark.django_db
def test_initiator_update_bplan_field(apiclient, bplan_factory, phase):
    bplan = bplan_factory(is_draft=False)
    phase.module.project = bplan
    phase.module.save()
    assert bplan.is_draft is False
    url = reverse(
        'bplan-detail',
        kwargs={
            'organisation_pk': bplan.organisation.pk,
            'pk': bplan.pk
        }
    )
    data = {
        "is_draft": "true",
    }
    user = bplan.organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    bplan = bplan_models.Bplan.objects.first()
    assert bplan.is_draft is True


@pytest.mark.django_db
def test_initiator_update_bplan_phase(apiclient, bplan_factory, phase):
    bplan = bplan_factory(is_draft=False)
    phase.module.project = bplan
    phase.module.save()
    assert bplan.is_draft is False
    url = reverse(
        'bplan-detail',
        kwargs={
            'organisation_pk': bplan.organisation.pk,
            'pk': bplan.pk
        }
    )
    data = {
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
    }
    user = bplan.organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    phase = phase_models.Phase.objects.get(module=phase.module)
    assert phase.start_date == parse("2013-01-01 17:00:00 UTC")
    assert phase.end_date == parse("2021-01-01 17:00:00 UTC")


@pytest.mark.django_db
def test_non_initiator_cannot_update_bplan(apiclient, bplan, user2):
    url = reverse(
        'bplan-detail',
        kwargs={
            'organisation_pk': bplan.organisation.pk,
            'pk': bplan.pk
        }
    )
    data = {}
    apiclient.force_authenticate(user=user2)
    response = apiclient.put(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_add_bplan_response(apiclient, organisation):
    url = reverse('bplan-list', kwargs={'organisation_pk': organisation.pk})
    data = {
        "name": "bplan-1",
        "description": "desc",
        "url": "https://bplan.net",
        "office_worker_email": "test@liqd.de",
        "start_date": "2013-01-01 18:00",
        "end_date": "2021-01-01 18:00",
    }
    user = organisation.initiators.first()
    apiclient.force_authenticate(user=user)
    response = apiclient.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    embed_code = \
        '<iframe height="500" style="width: 100%; min-height: 300px; ' \
        'max-height: 100vh" ' \
        'src="https://example.com/embed/projects/bplan-1/" ' \
        'frameborder="0"></iframe>'
    assert response.data == {
        'id': 1,
        'embed_code': embed_code
    }
