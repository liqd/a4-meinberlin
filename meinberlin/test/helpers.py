import os
from contextlib import contextmanager
from datetime import timedelta

import factory
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db.models.signals import post_save
from django.utils.encoding import smart_text
from easy_thumbnails.files import get_thumbnailer
from freezegun import freeze_time

from adhocracy4.test.helpers import redirect_target


@factory.django.mute_signals(post_save)
def setup_phase(phase_factory, item_factory, phase_content_class, **kwargs):
    phase_content = phase_content_class()
    phase = phase_factory(phase_content=phase_content, **kwargs)
    module = phase.module
    project = phase.module.project
    item = item_factory(module=module) if item_factory else None
    return phase, module, project, item


@factory.django.mute_signals(post_save)
def setup_users(project):
    anonymous = AnonymousUser()
    moderator = project.moderators.first()
    initiator = project.organisation.initiators.first()
    return anonymous, moderator, initiator


@contextmanager
def freeze_phase(phase):
    with freeze_time(phase.start_date + timedelta(seconds=1)):
        yield


@contextmanager
def freeze_pre_phase(phase):
    with freeze_time(phase.start_date - timedelta(seconds=1)):
        yield


@contextmanager
def freeze_post_phase(phase):
    with freeze_time(phase.end_date + timedelta(seconds=1)):
        yield


def assert_template_response(response, template_name, status_code=200):
    assert response.status_code == status_code
    response_template = response.template_name[0]
    assert response_template == template_name, \
        '{} != {}'.format(response_template, template_name)


def assert_dashboard_form_component_response(
        response, component, status_code=200):
    assert response.status_code == status_code
    assert str(component.form_title) in smart_text(response.content)


def assert_dashboard_form_component_edited(
        response, component, obj, data, status_code=200):
    obj.refresh_from_db()
    assert redirect_target(response) == \
        'dashboard-{}-edit'.format(component.identifier)
    for key in data.keys():
        attr = getattr(obj, key)
        value = data.get(key)
        assert attr == value, '{} != {}'.format(attr, value)


def createThumbnail(imagefield):
    thumbnailer = get_thumbnailer(imagefield)
    thumbnail = thumbnailer.generate_thumbnail(
        {'size': (800, 400), 'crop': 'smart'})
    thumbnailer.save_thumbnail(thumbnail)
    thumbnail_path = os.path.join(settings.MEDIA_ROOT, thumbnail.path)
    return thumbnail_path
