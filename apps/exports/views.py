import csv

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldError
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.views import generic

from adhocracy4.projects import mixins as project_mixins
from adhocracy4.ratings.models import Rating


class ItemExportView(project_mixins.ProjectMixin,
                     generic.ListView):
    fields = None
    exclude = None
    virtual = None
    model = None

    def __init__(self):
        super().__init__()
        if self.fields and self.exclude:
            raise FieldError()
        self._header, self._names = self._setup_fields()

    def _setup_fields(self):
        meta = self.model._meta
        exclude = self.exclude if self.exclude else []

        if self.fields:
            fields = [meta.get_field(name) for name in self.fields]
        else:
            fields = meta.get_fields()

        names = ['link']
        header = [_('Link')]
        for field in fields:
            if field.concrete \
                    and not (field.one_to_one and field.rel.parent_link) \
                    and field.attname not in exclude \
                    and field.attname not in names:

                names.append(field.attname)
                header.append(str(field.verbose_name))

        virtual = self.get_virtual_fields({})
        for name, head in virtual.items():
            if name not in names:
                names.append(name)
                header.append(head)

        return header, names

    def get_queryset(self):
        return super().get_queryset()

    def get_virtual_fields(self, virtual):
        virtual = super().get_virtual_fields(virtual)
        if 'link' not in virtual:
            virtual['link'] = _('Link')
        return virtual

    def get_link_data(self, item):
        return self.request.build_absolute_uri(item.get_absolute_url())

    def get_field_data(self, item, name):
        # Use custom getters if they are defined
        get_field_attr_name = 'get_%s_data' % name
        if hasattr(self, get_field_attr_name):
            get_field_attr = getattr(self, get_field_attr_name)

            if hasattr(get_field_attr, '__call__'):
                return get_field_attr(item)
            return get_field_attr

        # If item is a dict, return the fields data by key
        if name in item:
            return item['name']

        # Finally try to get the fields data as a property
        return getattr(item, name, '')

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = (
            'attachment; filename="ideas.csv"'
        )

        writer = csv.writer(response, lineterminator='\n',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(self._header)

        for item in self.get_queryset().all():
            data = [self.get_field_data(item, name) for name in self._names]
            writer.writerow(data)

        return response


class ItemExportWithRatesMixin:
    def get_virtual_fields(self, virtual):
        virtual = super().get_virtual_fields(virtual)
        if 'ratings_positive' not in virtual:
            virtual['ratings_positive'] = _('Positive ratings')
        if 'ratings_negative' not in virtual:
            virtual['ratings_negative'] = _('Negative ratings')

        return virtual

    def _count_ratings(self, item, value):
        ct = ContentType.objects.get_for_model(item)
        return Rating.objects.filter(content_type=ct, value=value).count()

    def get_ratings_positive_data(self, item):
        if hasattr(item, 'positive_rating_count'):
            return item.positive_rating_count

        if hasattr(item, 'ratings'):
            return self._count_ratings(item, Rating.POSITIVE)

        return 0

    def get_ratings_negative_data(self, item):
        if hasattr(item, 'negative_rating_count'):
            return item.negative_rating_count

        if hasattr(item, 'ratings'):
            return self._count_ratings(item, Rating.NEGATIVE)

        return 0


class ItemExportWithCommentCountMixin:
    def get_virtual_fields(self, virtual):
        virtual = super().get_virtual_fields(virtual)
        if 'comment_count' not in virtual:
            virtual['comment_count'] = _('Comment count')
        return virtual

    def get_comment_count_data(self, item):
        if hasattr(item, 'comment_count'):
            return item.comment_count

        if hasattr(item, 'comments'):
            return item.comments.count()

        return 0


class ItemExportWithCommentsMixin:
    COMMENT_FMT = '{date} - {username}\n{text}'

    def get_virtual_fields(self, virtual):
        virtual = super().get_virtual_fields(virtual)
        if 'comments' not in virtual:
            virtual['comments'] = _('Comments')
        return virtual

    def get_comment_data(self, item):
        if hasattr(item, 'comments'):
            comments = [self.COMMENT_FMT.format(
                date=comment.created.isoformat(),
                username=comment.creator.username,
                text=comment.comment)
                for comment in item.comments.all()]

            return '\n----\n'.join(comments)
