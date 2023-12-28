from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.exports.views import DashboardExportView
from meinberlin.apps.ideas import views as idea_views
from meinberlin.apps.ideas.views import IdeaListView
from meinberlin.apps.kiezkasse import forms
from meinberlin.apps.kiezkasse import models


class ProposalListView(IdeaListView):
    template_name = "meinberlin_kiezkasse/proposal_list.html"


class ProposalDetailView(idea_views.AbstractIdeaDetailView):
    model = models.Proposal
    queryset = (
        models.Proposal.objects.annotate_positive_rating_count().annotate_negative_rating_count()
    )
    permission_required = "meinberlin_kiezkasse.view_proposal"


class ProposalCreateView(idea_views.AbstractIdeaCreateView):
    model = models.Proposal
    form_class = forms.ProposalForm
    permission_required = "meinberlin_kiezkasse.add_proposal"
    template_name = "meinberlin_kiezkasse/proposal_create_form.html"


class ProposalUpdateView(idea_views.AbstractIdeaUpdateView):
    model = models.Proposal
    form_class = forms.ProposalForm
    permission_required = "meinberlin_kiezkasse.change_proposal"
    template_name = "meinberlin_kiezkasse/proposal_update_form.html"


class ProposalDeleteView(idea_views.AbstractIdeaDeleteView):
    model = models.Proposal
    success_message = _("Your budget request has been deleted")
    permission_required = "meinberlin_kiezkasse.change_proposal"
    template_name = "meinberlin_kiezkasse/proposal_confirm_delete.html"


class ProposalModerateView(idea_views.AbstractIdeaModerateView):
    model = models.Proposal
    permission_required = "meinberlin_kiezkasse.moderate_proposal"
    template_name = "meinberlin_kiezkasse/proposal_moderate_form.html"
    moderateable_form_class = forms.ProposalModerateForm


class ProposalDashboardExportView(DashboardExportView):
    template_name = "a4exports/export_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["export"] = reverse(
            "a4dashboard:kiezkasse-export", kwargs={"module_slug": self.module.slug}
        )
        context["comment_export"] = reverse(
            "a4dashboard:kiezkasse-comment-export",
            kwargs={"module_slug": self.module.slug},
        )
        return context
