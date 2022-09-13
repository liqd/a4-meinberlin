import pytest
from django.core import mail
from django.urls import reverse

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import redirect_target
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.kiezkasse import phases


@pytest.mark.django_db
def test_list_view(client, phase_factory, proposal_factory):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase)
    url = project.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_kiezkasse/proposal_list.html')


@pytest.mark.django_db
def test_detail_view(client, phase_factory, proposal_factory):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase)
    url = item.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_kiezkasse/proposal_detail.html')


@pytest.mark.django_db
def test_create_view(client, phase_factory, proposal_factory, user,
                     category_factory, area_settings_factory):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase)
    area_settings_factory(module=module)
    category = category_factory(module=module)
    url = reverse('meinberlin_kiezkasse:proposal-create',
                  kwargs={'module_slug': module.slug})
    with freeze_phase(phase):
        client.login(username=user.email, password='password')

        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_kiezkasse/proposal_create_form.html')

        data = {
            'name': 'Idea',
            'description': 'description',
            'category': category.pk,
            'budget': 123,
            'creator_contribution': True,
            'point': (0, 0),
            'point_label': 'somewhere'
        }
        response = client.post(url, data)
        assert redirect_target(response) == 'proposal-detail'


@pytest.mark.django_db
def test_moderate_view(client, phase_factory, proposal_factory, user,
                       area_settings_factory):
    phase, module, project, item = setup_phase(
        phase_factory, proposal_factory, phases.RequestPhase)
    area_settings_factory(module=module)
    url = reverse('meinberlin_kiezkasse:proposal-moderate',
                  kwargs={'pk': item.pk,
                          'year': item.created.year})
    project.moderators.set([user])
    with freeze_phase(phase):
        client.login(username=user.email, password='password')

        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_kiezkasse/proposal_moderate_form.html')

        data = {
            'moderator_feedback': 'test',
            'statement': 'its a statement'
        }
        response = client.post(url, data)
        assert redirect_target(response) == 'proposal-detail'

        # was the NotifyCreatorOnModeratorFeedback sent?
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == [item.creator.email]
        assert mail.outbox[0].subject.startswith('Rückmeldung')
