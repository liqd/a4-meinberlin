import pytest
from django.urls import reverse

from adhocracy4.projects.models import Project
from meinberlin.apps.organisations.models import Organisation
from meinberlin.apps.plans.models import Plan


@pytest.mark.django_db
def test_organisation_admin_form(client, user_factory, group_factory):

    admin = user_factory(is_superuser=True, is_staff=True)

    group1 = group_factory()
    group2 = group_factory()

    user = user_factory(groups=(group1, group2))
    assert user.groups.all().count() == 2

    client.force_login(admin)

    assert Organisation.objects.all().count() == 0

    url = reverse('admin:meinberlin_organisations_organisation_add')
    response = client.get(url)
    assert response.status_code == 200

    data = {'name': 'My Organisation'}
    response = client.post(url, data)
    assert response.status_code == 302

    assert Organisation.objects.all().count() == 1

    organisation = Organisation.objects.get(name='My Organisation')

    url = reverse(
        'admin:meinberlin_organisations_organisation_change',
        args=(organisation.id,))

    response = client.get(url)
    assert response.status_code == 200

    data = {'name': organisation.name,
            'groups': group1.id}
    response = client.post(url, data)

    assert response.status_code == 302
    organisation = Organisation.objects.get(name='My Organisation')
    assert organisation.groups.all().count() == 1
    assert organisation.groups.all().first() == group1

    data = {'name': organisation.name,
            'groups': [group1.id, group2.id]
            }
    response = client.post(url, data)

    msg = '{} is member of several groups ' \
          'in that organisation.'.format(user.email)
    assert msg in response.context['errors'][0]
    assert response.status_code == 200

    group1.user_set.remove(user)

    data = {'name': organisation.name,
            'groups': [group1.id, group2.id]
            }
    response = client.post(url, data)
    assert response.status_code == 302

    organisation = Organisation.objects.get(name='My Organisation')
    assert organisation.groups.all().count() == 2
    assert user.groups.all().count() == 1


@pytest.mark.django_db
def test_group_removal(client,
                       organisation,
                       project_factory,
                       plan_factory,
                       user_factory,
                       group_factory):

    group1 = group_factory()
    group2 = group_factory()
    organisation.groups.add(group1)
    project = project_factory(group=group1, organisation=organisation)
    plan = plan_factory(group=group1, organisation=organisation)

    assert Project.objects.all().count() == 1
    assert Project.objects.get(slug=project.slug).group == group1
    assert Plan.objects.all().count() == 1
    assert Plan.objects.get(id=plan.id).group == group1

    admin = user_factory(is_superuser=True, is_staff=True)
    client.force_login(admin)

    url = reverse(
        'admin:meinberlin_organisations_organisation_change',
        args=(organisation.id,))

    data = {'name': organisation.name,
            'groups': group2.id}
    response = client.post(url, data)

    assert response.status_code == 302
    assert Project.objects.get(slug=project.slug).group is None
    assert Plan.objects.get(id=plan.id).group is None
