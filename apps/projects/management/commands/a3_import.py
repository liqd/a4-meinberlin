from functools import lru_cache

import requests

from django.conf import settings
from django.core.management.base import CommandError
from django.utils import timezone

from adhocracy4.comments.models import Comment
from adhocracy4.maps.models import AreaSettings
from adhocracy4.modules.models import Module
from adhocracy4.phases.models import Phase
from adhocracy4.projects.models import Project
from adhocracy4.ratings.models import Rating

from apps.organisations.models import Organisation
from apps.users.models import User

from . import wagtail


def parse_dt(date_str):
    # remove colon in timezone offset
    parts = date_str.split(':')
    minutes_offset = parts.pop()
    date_str = ':'.join(parts) + minutes_offset

    date = timezone.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    return date


class A3ImportCommandMixin():

    project_content_type = None

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='a3 API url')
        parser.add_argument('api_user', type=str, help='a3 API admin user')
        parser.add_argument('api_password', type=str,
                            help='a3 API admin user password')
        parser.add_argument('creator', type=str, help='a4 creator username')
        parser.add_argument('wagtail', type=str, help='path to wagtail db')

    def handle(self, *args, **options):
        if settings.EMAIL_BACKEND != \
                'django.core.mail.backends.dummy.EmailBackend':
            raise CommandError('Set EMAIL_BACKEND to '
                               'django.core.mail.backends.dummy.EmailBackend.')

        wagtail_db = wagtail.create_db(options.get('wagtail'))

        url = options.get('url')
        user = options.get('api_user')
        password = options.get('api_password')
        creator = options.get('creator')

        default_creator = User.objects.get(username=creator)

        token = self.a3_login(url, user, password)

        orga_paths = self.a3_get_elements(
            url, token,
            'adhocracy_core.resources.organisation.IOrganisation', 'paths'
        )

        for orga_path in orga_paths:
            project_paths = self.a3_get_elements(
                orga_path, token, self.project_content_type, 'paths')
            if len(project_paths) == 0:
                continue

            orga_name = self.a3_get_sheet_field(
                orga_path, token,
                'adhocracy_core.sheets.name.IName', 'name'
            )
            orga, created = Organisation.objects.get_or_create(name=orga_name)

            self.stdout.write(
                'Importing projects for Organisation {} ...'.format(orga))
            for path in project_paths:
                wt = wagtail.get_adhocracy_process(wagtail_db, path)
                if not self.project_exists(wt):
                    self.import_project(token, path, orga, default_creator, wt)
                else:
                    self.stdout.write(
                        'Project {} already exists'.format(wt.get('name')))

        orga, created = Organisation.objects.get_or_create(name='Undefined')
        projects_without_orga = self.a3_get_elements(
            url, token, self.project_content_type, 'paths', depth='1')
        if len(projects_without_orga) > 0:
            self.stdout.write(
                'Importing projects without Organisation...')
            for path in projects_without_orga:
                wt = wagtail.get_adhocracy_process(wagtail_db, path)
                if not self.project_exists(wt):
                    self.import_project(token, path, orga, default_creator, wt)
                else:
                    self.stdout.write(
                        'Project {} already exists'.format(wt.get('name')))

    def import_project(self, token, path, organisation, creator, wt):
            raise NotImplementedError

    def project_exists(self, wt):
        name = wt.get('name', None)
        if name:
            return Project.objects.filter(name=name).exists()
        return False

    def a3_login(self, url, username, password):
        login_url = url + 'login_username'
        res = requests.post(
            login_url,
            json={'name': username, 'password': password}
        )
        if res.status_code != requests.codes.ok:
            raise CommandError('API user authentication failed.')
        return res.json()['user_token']

    def a3_get_elements(self, url, token, resource_type, elements,
                        depth='all'):
        query_url = '{}?content_type={}&depth={}&elements={}'.format(
            url, resource_type, depth, elements
        )
        if 'Version' in resource_type:
            query_url = query_url + '&tag=LAST'
        res = requests.get(query_url, headers={'X-User-Token': token})
        if res.status_code != requests.codes.ok:
            raise CommandError('Request failed for URL: {}'.format(query_url))
        data = res.json()
        paths = data['data']['adhocracy_core.sheets.pool.IPool']['elements']
        return paths

    @lru_cache(maxsize=None)
    def a3_get_resource(self, resource_url, token):
        res = requests.get(resource_url, headers={'X-User-Token': token})
        if res.status_code != requests.codes.ok:
            raise CommandError('Request failed for URL: {}'.format(
                resource_url)
            )
        data = res.json()
        return data

    def a3_get_sheet_field(self, resource_url, token, sheet, field):
        data = self.a3_get_resource(resource_url, token)
        sheet_field_value = data['data'][sheet][field]
        return sheet_field_value

    def a3_get_last_version(self, resorce_path, token):
        return self.a3_get_sheet_field(
            resorce_path, token, 'adhocracy_core.sheets.tags.ITags', 'LAST')

    def a3_get_creation_date(self, path, token):
        date_str = self.a3_get_sheet_field(
            path, token,
            'adhocracy_core.sheets.metadata.IMetadata', 'creation_date')
        date = parse_dt(date_str)
        return date

    def a3_get_modification_date(self, path, token):
        date_str = self.a3_get_sheet_field(
            path, token,
            'adhocracy_core.sheets.metadata.IMetadata', 'modification_date')
        date = parse_dt(date_str)
        return date

    def a3_get_user_by_path(self, path, token):
        username = self.a3_get_sheet_field(
            path, token,
            'adhocracy_core.sheets.principal.IUserBasic', 'name')
        user = User.objects.get(username=username)
        return user

    def a3_import_comment(self, token, comment_path, object_path,
                          content_object):
        comment = None
        comment_resource = self.a3_get_resource(comment_path, token)
        data = comment_resource['data']
        metadata_sheet = data['adhocracy_core.sheets.metadata.IMetadata']
        is_hidden = metadata_sheet['hidden']
        user_path = metadata_sheet['creator']
        creation_date = parse_dt(metadata_sheet['creation_date'])
        last_version_path = self.a3_get_last_version(comment_path, token)
        last_version = self.a3_get_resource(last_version_path, token)
        data = last_version['data']
        if is_hidden == 'false' and user_path:
            comment_sheet = data['adhocracy_core.sheets.comment.IComment']
            object = comment_sheet['refers_to']
            if object_path == object:
                user = self.a3_get_user_by_path(user_path, token)
                content = comment_sheet['content']
                comment = Comment.objects.create(
                    comment=content,
                    creator=user,
                    content_object=content_object,
                    created=creation_date,
                )
        return comment

    def a3_import_comments(self, token, object_path, content_object):
        comments_path = self.a3_get_sheet_field(
            object_path, token,
            'adhocracy_core.sheets.comment.ICommentable', 'post_pool')
        comment_paths = self.a3_get_elements(
            comments_path, token,
            'adhocracy_core.resources.comment.IComment', 'paths')
        for comment_path in comment_paths:
            comment = self.a3_import_comment(
                token, comment_path, object_path, content_object)

            if comment:
                comment_version_path = \
                    self.a3_get_last_version(comment_path, token)
                self.a3_import_ratings(token, comment_version_path, comment)
                self.a3_import_comment_replies(
                    token, comment_paths, comment_version_path, comment)

    def a3_import_comment_replies(self, token, comment_paths,
                                  comment_version_path, content_object):
        for comment_path in comment_paths:
            reply = self.a3_import_comment(
                token, comment_path, comment_version_path, content_object)
            if reply:
                reply_version_path = \
                    self.a3_get_last_version(comment_path, token)
                self.a3_import_ratings(token, comment_version_path, reply)
                self.a3_import_comment_replies(
                    token, comment_paths, reply_version_path,
                    content_object)

    def a3_import_ratings(self, token, object_path, content_object):
        rates_path = self.a3_get_sheet_field(
            object_path, token,
            'adhocracy_core.sheets.rate.IRateable', 'post_pool'
        )
        rates_content = self.a3_get_elements(
            rates_path, token,
            'adhocracy_core.resources.rate.IRateVersion', 'content')
        for rate_resource in rates_content:
            data = rate_resource['data']
            metadata_sheet = data['adhocracy_core.sheets.metadata.IMetadata']
            is_hidden = metadata_sheet['hidden']
            rate_sheet = data['adhocracy_core.sheets.rate.IRate']
            user_path = rate_sheet['subject']
            is_object = rate_sheet['object'] == object_path
            if is_hidden == 'false' and user_path and is_object:
                creation_date = parse_dt(metadata_sheet['creation_date'])
                user = self.a3_get_user_by_path(user_path, token)
                rate_value = int(rate_sheet['rate'])
                if rate_value != 0:
                    Rating.objects.create(
                        value=rate_value,
                        creator=user,
                        content_object=content_object,
                        created=creation_date,
                    )

    def a3_get_rates(self, resource_path, token, object_path):
        rates_path = resource_path + 'rates/'
        rates = []
        rates_content = self.a3_get_elements(
            rates_path, token,
            'adhocracy_core.resources.rate.IRateVersion', 'content')
        for rate in rates_content:
            data = rate['data']
            is_hidden = \
                data['adhocracy_core.sheets.metadata.IMetadata']['hidden']
            rate_sheet = data['adhocracy_core.sheets.rate.IRate']
            user_path = rate_sheet['subject']
            is_object = rate_sheet['object'] == object_path
            if is_hidden == 'false' and user_path and is_object:
                user = self.a3_get_user_by_path(user_path, token)
                rate_value = int(rate_sheet['rate'])
                if rate_value != 0:
                    rates.append((user, rate_value))
        return rates

    def a3_import_area_sttings(self, location_path, token, module):
        coordinates = self.a3_get_sheet_field(
            location_path, token,
            'adhocracy_core.sheets.geo.IMultiPolygon', 'coordinates')
        polygon = {
            'type': 'FeatureCollection',
            'features': [
                {'type': 'Feature',
                 'properties': {},
                 'geometry': {
                     'type': 'Polygon',
                     'coordinates': coordinates[0]}}]}
        AreaSettings.objects.create(
            module=module,
            polygon=polygon
        )

    def a3_get_dates(self, path, token, wt):
        creation_date = wt.get('created')
        if not creation_date:
            creation_date = self.a3_get_creation_date(path, token)
        modification_date = wt.get('modified')
        if not modification_date:
            modification_date = self.a3_get_modification_date(path, token)
        return (creation_date, modification_date)

    def create_project(self, organisation, name, description, info, start_date,
                       end_date, is_draft, is_archived, typ, phase_contents):
        project = Project.objects.create(
            name=name,
            description=description,
            information=info,
            is_draft=is_draft,
            is_archived=is_archived,
            typ=typ,
            organisation=organisation,
            created=start_date,
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
