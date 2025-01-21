from django import forms
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _
from wagtail.admin.forms.choosers import BaseFilterForm
from wagtail.admin.views.generic.chooser import ChooseResultsViewMixin
from wagtail.admin.views.generic.chooser import ChooseView
from wagtail.admin.viewsets.chooser import ChooserViewSet

from adhocracy4.projects.enums import Access


class UserSearchFilterMixin(BaseFilterForm):
    show_past = forms.BooleanField(
        required=False,
        label=_("Show past projects"),
        widget=forms.CheckboxInput(attrs={"data-chooser-modal-search-filter": True}),
    )
    q = forms.CharField(required=False, label=_("Search"))

    def filter(self, objects):
        objects = super().filter(objects)
        now = timezone.now()
        show_past = self.cleaned_data.get("show_past")
        query = self.cleaned_data.get("q")

        objects = objects.filter(
            Q(access=Access.PUBLIC) | Q(access=Access.SEMIPUBLIC), is_draft=False
        )

        if not show_past:
            objects = objects.filter(
                Q(
                    module__phase__start_date__lte=now,
                    module__phase__end_date__gt=now,
                    module__is_draft=False,
                )
                | Q(module__phase__start_date__gt=now, module__is_draft=False)
            ).distinct()

        if query:
            objects = objects.filter(name__icontains=query)
            self.is_searching = True
            self.search_query = query
        return objects


class BaseUserChooseView(ChooseView):
    filter_form_class = UserSearchFilterMixin


class UserChooseResultsView(ChooseResultsViewMixin, BaseUserChooseView):
    pass


class ProjectChooserViewSet(ChooserViewSet):
    model = "a4projects.Project"

    icon = "folder"
    choose_one_text = _("Choose a project")
    choose_another_text = _("Choose another project")
    choose_view_class = BaseUserChooseView
    preserve_url_parameters = ["q", "show_past"]
    choose_results_view_class = UserChooseResultsView
    per_page = 30


project_chooser_viewset = ProjectChooserViewSet("project_chooser")
