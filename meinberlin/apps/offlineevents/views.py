from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views import generic

from adhocracy4.dashboard import mixins
from adhocracy4.projects.mixins import ProjectMixin
from adhocracy4.rules import mixins as rules_mixins

from . import forms
from . import models


class OfflineEventModuleDetailView(
    ProjectMixin, rules_mixins.PermissionRequiredMixin, generic.TemplateView
):
    """Simple view for offline event modules when called as phase view.

    This view renders the module detail template. The module is already
    in kwargs from PhaseDispatchMixin.
    """

    get_context_from_object = False
    template_name = "meinberlin_projects/module_offline_event_detail.html"
    permission_required = "a4projects.view_project"

    def get_permission_object(self):
        return self.project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        context["module"] = self.module

        # Add offline event item context (same as ModuleDetailview)
        if self.module:
            item = self.module.item_set.first()
            context["offline_event_item"] = item

        return context


# Offline Events Modul Area


class OfflineEventModuleDashboardView(
    ProjectMixin,
    mixins.DashboardBaseMixin,
    mixins.DashboardComponentMixin,
    mixins.DashboardComponentFormSignalMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    model = models.OfflineEventItem
    template_name = "meinberlin_offlineevents/offlineevent_module_dashboard_form.html"
    permission_required = "a4projects.change_project"
    form_class = forms.OfflineEventBasicForm
    success_message = _("The module has been updated.")

    def get_permission_object(self):
        return self.project

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.module = self.module
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return models.OfflineEventItem.objects.filter(module=self.module).first()


class OfflineEventSettingsDashboardView(
    ProjectMixin,
    mixins.DashboardBaseMixin,
    mixins.DashboardComponentMixin,
    mixins.DashboardComponentFormSignalMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    model = models.OfflineEventItem
    template_name = "meinberlin_offlineevents/offlineevent_settings_dashboard_form.html"
    permission_required = "a4projects.change_project"
    form_class = forms.OfflineEventItemForm
    success_message = _("The module has been updated.")

    def get_permission_object(self):
        return self.project

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.module = self.module
        return super().form_valid(form)

    def get_object(self, queryset=None):
        obj = models.OfflineEventItem.objects.filter(module=self.module).first()
        if obj is None:
            obj = models.OfflineEventItem.objects.create(
                module=self.module, creator=self.request.user
            )
        return obj
