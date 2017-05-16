import pytz
import requests

from django.core.management.base import CommandError
from django.utils import timezone

from adhocracy4.modules.models import Module
from adhocracy4.phases.models import Phase
from adhocracy4.projects.models import Project


def a3_login(url, headers, username, password):
    login_url = url + 'login_username'
    res = requests.post(
        login_url,
        json={'name': username, 'password': password}
    )
    if res.status_code != requests.codes.ok:
        raise CommandError('API user authentication failed.')
    headers['X-User-Token'] = res.json()['user_token']


def a3_get_elements(url, headers, resource_type, elements):
    query_url = '{}?content_type={}&depth=all&elements={}'.format(
        url, resource_type, elements
    )
    res = requests.get(query_url, headers=headers)
    if res.status_code != requests.codes.ok:
        raise CommandError('Request failed for URL: {}'.format(query_url))
    data = res.json()
    paths = data['data']['adhocracy_core.sheets.pool.IPool']['elements']
    return paths


def a3_get_sheet_field(resource_url, headers, sheet, field):
    res = requests.get(resource_url, headers=headers)
    if res.status_code != requests.codes.ok:
        raise CommandError('Request failed for URL: {}'.format(
            resource_url)
        )
    data = res.json()
    sheet_field_value = data['data'][sheet][field]
    return sheet_field_value


def a3_get_last_version(resorce_path, headers):
    return a3_get_sheet_field(
        resorce_path, headers, 'adhocracy_core.sheets.tags.ITags', 'LAST')


def a3_get_creation_date(path, headers):
    date_str = a3_get_sheet_field(
        path, headers,
        'adhocracy_core.sheets.metadata.IMetadata', 'creation_date')
    date = timezone.datetime.strptime(date_str[:19], '%Y-%m-%dT%H:%M:%S')
    date = date.astimezone(pytz.utc)
    return date


def a3_get_modification_date(path, headers):
    date_str = a3_get_sheet_field(
        path, headers,
        'adhocracy_core.sheets.metadata.IMetadata', 'modification_date')
    date = timezone.datetime.strptime(date_str[:19], '%Y-%m-%dT%H:%M:%S')
    date = date.astimezone(pytz.utc)
    return date


def create_project(organisation, name, description, info, start_date, end_date,
                   typ, phase_contents):
    project = Project.objects.create(
        name=name,
        description=description,
        information=info,
        is_draft=False,
        is_archived=True,
        typ=typ,
        organisation=organisation,
    )

    module = Module.objects.create(
        name=project.slug + '_module',
        weight=1,
        project=project,
    )

    phase_start = start_date
    phase_duration = (end_date - start_date) / len(phase_contents)
    for phase_content in phase_contents:
        phase_end = phase_start + phase_duration
        Phase.objects.create(
            name=phase_content.name,
            description=phase_content.description,
            type=phase_content.identifier,
            module=module,
            start_date=phase_start,
            end_date=phase_end
        )
        phase_start = phase_end

    return (project, module)
