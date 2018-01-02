from datetime import datetime

import django_filters
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from adhocracy4.filters import views as filter_views
from adhocracy4.filters import widgets as filters_widgets
from adhocracy4.filters.filters import DefaultsFilterSet
from adhocracy4.filters.filters import FreeTextFilter
from adhocracy4.filters.widgets import DropdownLinkWidget
from adhocracy4.projects import models as project_models

from . import query

User = get_user_model()


class OrderingWidget(DropdownLinkWidget):
    label = _('Ordering')
    right = True


class OrganisationWidget(DropdownLinkWidget):
    label = _('Organisation')


class FreeTextFilterWidget(filters_widgets.FreeTextFilterWidget):
    label = _('Search')


class ArchivedWidget(DropdownLinkWidget):
    label = _('Archived')

    def __init__(self, attrs=None):
        choices = (
            ('', _('All')),
            ('false', _('No')),
            ('true', _('Yes')),
        )
        super().__init__(attrs, choices)


class YearWidget(DropdownLinkWidget):
    label = _('Year')

    def __init__(self, attrs=None):
        choices = (('', _('Any')),)
        now = datetime.now().year
        try:
            first_year = project_models.Project.objects.earliest('created').\
                created.year
        except project_models.Project.DoesNotExist:
            first_year = now
        for year in range(now, first_year - 1, -1):
            choices += (year, year),
        super().__init__(attrs, choices)


class ProjectFilterSet(DefaultsFilterSet):

    defaults = {
        'is_archived': 'false'
    }

    ordering = django_filters.OrderingFilter(
        choices=(
            ('-created', _('Most recent')),
        ),
        empty_label=None,
        widget=OrderingWidget,
    )

    search = FreeTextFilter(
        widget=FreeTextFilterWidget,
        fields=['name', 'description',
                'projectcontainer__projects__name']
    )

    organisation = django_filters.ModelChoiceFilter(
        queryset=apps.get_model(settings.A4_ORGANISATIONS_MODEL).objects
                     .order_by('name'),
        widget=OrganisationWidget,
    )

    is_archived = django_filters.BooleanFilter(
        widget=ArchivedWidget
    )

    created = django_filters.NumberFilter(
        name='created',
        lookup_expr='year',
        widget=YearWidget,
    )

    class Meta:
        model = project_models.Project
        fields = ['search', 'organisation', 'is_archived', 'created']


class ProjectListView(filter_views.FilteredListView):
    model = project_models.Project
    paginate_by = 16
    filter_set = ProjectFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()\
            .filter(
                # Show only published projects
                is_draft=False)\
            .filter(
                # Do not include archived bplan projects
                Q(is_archived=False) |
                Q(externalproject__bplan=None))\
            .filter(
                # Do not include projects belonging to containers
                containers=None)
        # Show only projects viewable by the current user
        queryset = query.filter_viewable(queryset, self.request.user)
        # List every project at most once
        return queryset.distinct()
