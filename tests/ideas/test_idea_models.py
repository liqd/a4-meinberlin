import os

import pytest
from django.conf import settings
from django.core.urlresolvers import reverse

from adhocracy4.comments import models as comments_models
from adhocracy4.ratings import models as rating_models
from meinberlin.apps.ideas import models as idea_models
from meinberlin.test.helpers import createThumbnail


@pytest.mark.django_db
def test_absolute_url(idea):
    url = reverse('meinberlin_ideas:idea-detail',
                  kwargs={'pk': '{:05d}'.format(idea.pk),
                          'year': idea.created.year})
    assert idea.get_absolute_url() == url


@pytest.mark.django_db
def test_save(idea):
    assert '<script>' not in idea.description


@pytest.mark.django_db
def test_str(idea):
    idea_string = idea.__str__()
    assert idea_string == idea.name


@pytest.mark.django_db
def test_project(idea):
    assert idea.module.project == idea.project


@pytest.mark.django_db
def test_delete_idea(idea_factory, comment_factory, rating_factory, ImagePNG):
    idea = idea_factory(image=ImagePNG)
    image_path = os.path.join(settings.MEDIA_ROOT, idea.image.path)
    thumbnail_path = createThumbnail(idea.image)

    for i in range(5):
        comment_factory(content_object=idea)
    comment_count = comments_models.Comment.objects.all().count()
    assert comment_count == len(idea.comments.all())

    rating_factory(content_object=idea)
    rating_count = rating_models.Rating.objects.all().count()

    assert os.path.isfile(image_path)
    assert os.path.isfile(thumbnail_path)
    count = idea_models.Idea.objects.all().count()
    assert count == 1
    assert comment_count == 5
    assert rating_count == 1

    idea.delete()
    assert not os.path.isfile(image_path)
    assert not os.path.isfile(thumbnail_path)
    count = idea_models.Idea.objects.all().count()
    comment_count = comments_models.Comment.objects.all().count()
    rating_count = rating_models.Rating.objects.all().count()
    assert count == 0
    assert comment_count == 0
    assert rating_count == 0


@pytest.mark.django_db
def test_image_deleted_after_update(idea_factory, ImagePNG):
    idea = idea_factory(image=ImagePNG)
    image_path = os.path.join(settings.MEDIA_ROOT, idea.image.path)
    thumbnail_path = createThumbnail(idea.image)

    assert os.path.isfile(image_path)
    assert os.path.isfile(thumbnail_path)

    idea.image = None
    idea.save()

    assert not os.path.isfile(image_path)
    assert not os.path.isfile(thumbnail_path)
