import itertools

from django.urls import reverse

from meinberlin.apps.dashboard import is_event_module

from . import models


class ProjectDetailDisplayMixin:
    """Shared context for project detail and dashboard preview views."""

    def get_project_display_context(self, **kwargs):
        context = super().get_context_data(**kwargs)

        modules_qs = self.project.modules.prefetch_related("item_set")
        all_modules = list(
            itertools.chain(
                modules_qs.running_modules(),
                modules_qs.future_modules(),
                modules_qs.past_modules(),
            )
        )

        context["modules"] = [m for m in all_modules if not is_event_module(m)]
        context["offline_modules"] = [m for m in all_modules if is_event_module(m)]

        context["edit_link"] = reverse(
            "a4dashboard:project-edit", kwargs={"project_slug": self.project.slug}
        )
        return models.ProjectInsight.update_context(self.project, context)

    def get_context_data(self, **kwargs):
        return self.get_project_display_context(**kwargs)
