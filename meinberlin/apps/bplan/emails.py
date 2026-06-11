from django.conf import settings
from django.urls import reverse

from meinberlin.apps.contrib.emails import Email


class OfficeWorkerUpdateConfirmation(Email):
    template_name = "meinberlin_bplan/emails/office_worker_update_confirmation"

    def get_receivers(self):
        return [self.object.office_worker_email]

    def get_context(self):
        context = super().get_context()
        context["contact_email"] = settings.CONTACT_EMAIL
        context["project_list_url"] = reverse("meinberlin_plans:plan-list")
        return context
