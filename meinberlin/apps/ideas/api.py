from typing import Dict
from typing import List
from typing import Tuple

from django.db.models import Model
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.filters import BaseFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import BasePagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from adhocracy4.api.mixins import ModuleMixin
from adhocracy4.api.permissions import RulesPermission
from adhocracy4.api.permissions import ViewSetRulesPermission
from adhocracy4.categories import get_category_icon_url
from adhocracy4.categories import has_icons
from adhocracy4.categories.models import Category
from adhocracy4.categories.models import CategoryAlias
from adhocracy4.labels.models import Label
from adhocracy4.labels.models import LabelAlias
from adhocracy4.modules.models import Module
from adhocracy4.modules.predicates import is_allowed_moderate_project
from meinberlin.apps.contrib.api import APIPagination
from meinberlin.apps.contrib.filters import DefaultsRestFilterSet
from meinberlin.apps.contrib.filters import NoExceptionFilterBackend
from meinberlin.apps.contrib.filters import OrderingFilterWithDailyRandom
from meinberlin.apps.contrib.mixins import LocaleInfoMixin
from meinberlin.apps.ideas.filters import IdeaFilterSet
from meinberlin.apps.ideas.models import Idea
from meinberlin.apps.ideas.serializers import IdeaSerializer
from meinberlin.apps.moderationtasks.models import ModerationTask
from meinberlin.apps.moderatorfeedback.models import (
    DEFAULT_CHOICES as moderator_status_default_choices,
)


class IdeaFilterInfoMixin:
    """Add the filter information to the API response.

    Any class extending this need to import the following mixins:
        rest_framework.mixins.ListModelMixin
        adhocracy4.api.mixins.ModuleMixin (or some other mixin that fetches the module)
    """

    def list(self, request: Request, *args, **kwargs) -> Response:
        filters = {}

        # category filter
        category_choices, category_icons = self.get_category_choices_and_icons()
        if category_choices:
            filters["category"] = {
                "label": self.get_category_label(),
                "choices": category_choices,
            }
            if category_icons:
                filters["category"]["icons"] = category_icons

        # label filter
        label_choices = self.get_label_choices()
        if label_choices:
            filters["labels"] = {
                "label": self.get_label_label(),
                "choices": label_choices,
            }

        # moderator feedback filter
        moderator_status_choices = [("", _("All"))] + [
            choice for choice in moderator_status_default_choices
        ]

        filters["moderator_status"] = {
            "label": _("Status"),
            "choices": moderator_status_choices,
        }

        # moderation task filter, only show to moderators
        if is_allowed_moderate_project(request.user, self.module):
            moderation_task_choices = self.get_moderation_task_choices()
            if moderation_task_choices:
                filters["open_task"] = {
                    "label": _("Open tasks"),
                    "choices": moderation_task_choices,
                }

        # ordering filter
        ordering_choices = self.get_ordering_choices(request)
        default_ordering = self.get_default_ordering()
        filters["ordering"] = {
            "label": _("Ordering"),
            "choices": ordering_choices,
            "default": default_ordering,
        }

        response = super().list(request, args, kwargs)
        response.data["filters"] = filters
        return response

    def get_category_choices_and_icons(
        self,
    ) -> Tuple[List[Tuple[str, str]], Dict[str, str]]:
        """Create the list of categories and icons for this module.

        Returns:
            A tuple with the category choices and category icons.
        """
        category_choices = category_icons = None
        categories = Category.objects.filter(module=self.module)
        if categories:
            category_choices = [
                ("", _("All")),
            ]
            if has_icons(self.module):
                category_icons = []
            for category in categories:
                category_choices += ((str(category.pk), category.name),)
                if has_icons(self.module):
                    icon_name = getattr(category, "icon", None)
                    icon_url = get_category_icon_url(icon_name)
                    category_icons += ((str(category.pk), icon_url),)
        return category_choices, category_icons

    def get_category_label(self) -> str:
        """Get the category label for this module

        Returns:
            category alias if set, otherwise translation of "Category".
        """
        category_alias = CategoryAlias.get_category_alias(self.module)
        if category_alias:
            return category_alias.title
        return _("Category")

    def get_label_choices(self) -> List[Tuple[str, str]]:
        """Get the list of label choices.

        Returns:
            List of tuples containing the label pk and name
        """
        label_choices = None
        labels = Label.objects.filter(module=self.module)
        if labels:
            label_choices = [
                ("", _("All")),
            ]
            for label in labels:
                label_choices += ((str(label.pk), label.name),)

        return label_choices

    def get_label_label(self) -> str:
        """Get the label alias.

        Returns:
            label alias if set, otherwise translation of "Label".
        """
        label_alias = LabelAlias.get_label_alias(self.module)
        if label_alias:
            return label_alias.title
        return _("Label")

    def get_moderation_task_choices(self) -> List[Tuple[str, str]]:
        """Get the moderation task choices.

        Returns:
            List of tuples containing the task pk and name.
        """
        moderation_task_choices = None
        moderation_tasks = ModerationTask.objects.filter(module=self.module)
        if moderation_tasks:
            moderation_task_choices = [
                ("", _("All")),
            ]
            for task in moderation_tasks:
                moderation_task_choices += ((str(task.pk), task.name),)

        return moderation_task_choices

    def get_ordering_choices(self, request: Request) -> List[Tuple[str, str]]:
        """Get the ordering choices.

        Arguments:
            request: may be used in subclasses.

        Returns:
            List of tuples containing the ordering and the name of the ordering.
        """
        ordering_choices = [
            ("-created", _("Most recent")),
        ]
        # only show sort by rating when rating is allowed at anytime in module
        # like "view_rate_count" from PermissionInfoMixin
        if self.module.has_feature("rate", self.model):
            ordering_choices += (("-positive_rating_count", _("Most popular")),)

        ordering_choices += (
            ("-comment_count", _("Most commented")),
            ("dailyrandom", _("Random")),
        )

        return ordering_choices

    def get_default_ordering(self) -> str:
        """Return current default of ordering filter."""
        return "dailyrandom"


class PermissionInfoMixin:
    def list(self, request: Request, *args, **kwargs) -> Response:
        """Add the permission information to the API response.

        Any class extending this need to import the following mixins:
            rest_framework.mixins.ListModelMixin
            adhocracy4.api.mixins.ModuleMixin (or some other mixin that fetches the module)
        """
        response = super().list(request, args, kwargs)
        permissions = {
            "view_comment_count": self.module.has_feature("comment", self.model),
            "view_rate_count": self.module.has_feature("rate", self.model),
        }

        response.data["permissions"] = permissions
        return response


class BaseIdeaViewSet(
    LocaleInfoMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Base class for all idea ViewSets.

    Any class extending this needs to import or extend the following mixins:
        adhocracy4.api.mixins.ModuleMixin
        meinberlin.apps.ideas.api.IdeaFilterInfoMixin
        meinberlin.apps.ideas.api.PermissionInfoMixin

    These imports are not included in this base class as their order
    of import might need to change in a subclass.
    """

    model: Model = Idea
    pagination_class: BasePagination = APIPagination
    serializer_class: ModelSerializer = IdeaSerializer
    permission_classes: List[RulesPermission] = (ViewSetRulesPermission,)
    filter_backends: List[BaseFilterBackend] = (
        NoExceptionFilterBackend,
        OrderingFilterWithDailyRandom,
        SearchFilter,
    )
    # this is used by IdeaFilterBackend
    filterset_class: DefaultsRestFilterSet = IdeaFilterSet

    ordering_fields: List[str] = (
        "created",
        "comment_count",
        "positive_rating_count",
        "dailyrandom",
    )
    search_fields: List[str] = ("name", "ref_number")

    @property
    def ordering(self) -> List[str]:
        return ["dailyrandom"]

    def get_permission_object(self) -> Module:
        return self.module

    def get_queryset(self) -> QuerySet:
        ideas = (
            self.model.objects.filter(module=self.module)
            .annotate_comment_count()
            .annotate_positive_rating_count()
            .annotate_negative_rating_count()
            .annotate_reference_number()
            .order_by("-created")
        )
        return ideas


class IdeaViewSet(
    ModuleMixin, IdeaFilterInfoMixin, PermissionInfoMixin, BaseIdeaViewSet
):
    """Provides a basic ViewSet for ideas."""

    pass
