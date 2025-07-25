import datetime
from urllib.parse import parse_qs
from urllib.parse import urlparse

import django_filters
from django.shortcuts import redirect
from django.urls import resolve
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.categories import filters as category_filters
from adhocracy4.exports.views import DashboardExportView
from adhocracy4.filters import filters as a4_filters
from adhocracy4.labels import filters as label_filters
from adhocracy4.modules.predicates import module_is_between_phases
from adhocracy4.projects.mixins import DisplayProjectOrModuleMixin
from meinberlin.apps.ideas import views as idea_views
from meinberlin.apps.moderatorremark.forms import ModeratorRemarkForm
from meinberlin.apps.projects.views import ArchivedWidget
from meinberlin.apps.votes.forms import TokenForm
from meinberlin.apps.votes.models import VotingToken

from . import forms
from . import models

TOKEN_SESSION_EXPIRE = datetime.timedelta(hours=12)


def get_ordering_choices(view):
    choices = (("-created", _("Most recent")),)
    if view.module.has_feature("rate", models.Proposal):
        choices += (("-positive_rating_count", _("Most popular")),)
    elif view.module.has_feature("support", models.Proposal):
        choices += (("-positive_rating_count", _("Most support")),)
    choices += (
        ("-comment_count", _("Most commented")),
        ("dailyrandom", _("Random")),
    )
    return choices


def get_default_ordering(view):
    if module_is_between_phases(
        "meinberlin_budgeting:support", "meinberlin_budgeting:voting", view.module
    ):
        return "-positive_rating_count"
    elif (
        view.module.has_feature("vote", models.Proposal)
        and view.module.module_has_finished
    ):
        return "-token_vote_count"
    return "dailyrandom"


class ProposalFilterSet(a4_filters.DefaultsFilterSet):
    defaults = {"is_archived": "false"}
    ordering = a4_filters.DistinctOrderingWithDailyRandomFilter(
        choices=get_ordering_choices
    )
    is_archived = django_filters.BooleanFilter(widget=ArchivedWidget)

    class Meta:
        model = models.Proposal
        fields = ["category", "labels", "is_archived"]

    def __init__(self, data, *args, **kwargs):
        self.defaults["ordering"] = get_default_ordering(kwargs["view"])
        self.base_filters["category"] = category_filters.CategoryAliasFilter(
            module=kwargs["view"].module, field_name="category"
        )
        self.base_filters["labels"] = label_filters.LabelAliasFilter(
            module=kwargs["view"].module, field_name="labels"
        )
        super().__init__(data, *args, **kwargs)


class ProposalListView(idea_views.AbstractIdeaListView, DisplayProjectOrModuleMixin):
    model = models.Proposal
    filter_set = ProposalFilterSet

    def has_valid_token_in_session(self, request):
        """Return whether a valid token is stored in the session.

        The token is valid if it is valid for the respective module.
        """
        if "voting_tokens" in request.session:
            module_key = str(self.module.id)
            if module_key in request.session["voting_tokens"]:
                return (
                    VotingToken.get_voting_token_by_hash(
                        token_hash=request.session["voting_tokens"][module_key],
                        module=self.module,
                    )
                    is not None
                )
        return False

    def dispatch(self, request, **kwargs):
        self.mode = request.GET.get("mode", "map")
        if self.mode == "map":
            self.paginate_by = 0
        return super().dispatch(request, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(module=self.module)

    def get_context_data(self, **kwargs):
        if "token_form" not in kwargs:
            token_form = TokenForm(module_id=self.module.id)
            kwargs["token_form"] = token_form
        kwargs["valid_token_present"] = self.has_valid_token_in_session(self.request)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        token_form = TokenForm(request.POST, module_id=self.module.id)
        if token_form.is_valid():
            if "voting_tokens" in request.session:
                request.session["voting_tokens"][
                    str(self.module.id)
                ] = token_form.cleaned_data["token"]
                request.session.modified = True
            else:
                request.session["voting_tokens"] = {
                    str(self.module.id): token_form.cleaned_data["token"]
                }
            request.session["token_expire_date"] = (
                datetime.datetime.now() + TOKEN_SESSION_EXPIRE
            ).timestamp()
            kwargs["valid_token_present"] = True
            # redirect to the list view, but keep filters after successful
            # token addition
            list_url = request.path
            parameter = request.GET.copy()
            if not parameter.get("mode") or "list" not in parameter.get("mode"):
                parameter.setlist("mode", ["list"])
            encoded_parameter = "?" + parameter.urlencode()
            return redirect(list_url + encoded_parameter)
        # stay on the same page if the token form has errors,
        # add the form including errors so that they are displayed.
        kwargs["token_form"] = token_form
        context = super().get_context_data(**kwargs)
        return self.render_to_response(context)


class ProposalDetailView(idea_views.AbstractIdeaDetailView):
    model = models.Proposal
    queryset = (
        models.Proposal.objects.annotate_positive_rating_count()
        .annotate_negative_rating_count()
        .annotate_token_vote_count()
    )
    permission_required = "meinberlin_budgeting.view_proposal"

    def get_back(self):
        """
        Get last page to return to if was project or module view.

        To make sure all the filters and the display mode (map or list)
        are remembered when going back, we check if the referer is a
        module or project detail view and add the appropriate back url.
        """
        back_link = self.module.get_absolute_url
        back_string = _("map")
        if "Referer" in self.request.headers:
            referer = self.request.headers["Referer"]
            parsed_url = urlparse(referer)
            match = resolve(parsed_url.path)
            if match.url_name == "project-detail" or match.url_name == "module-detail":
                if "mode" in parse_qs(parsed_url.query):
                    back_mode = parse_qs(parsed_url.query)["mode"][0]
                    if back_mode == "list":
                        back_string = _("list")
                back_link = referer + "#proposal_{}".format(self.object.id)
                return back_link, back_string
            return back_link, back_string
        return back_link, back_string

    def has_valid_token_in_session(self, request):
        """Return whether a valid token is stored in the session.

        The token is valid if it is valid for the respective module.
        """
        if "voting_tokens" in request.session:
            module_key = str(self.module.id)
            if module_key in request.session["voting_tokens"]:
                return (
                    VotingToken.get_voting_token_by_hash(
                        token_hash=request.session["voting_tokens"][module_key],
                        module=self.module,
                    )
                    is not None
                )
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        back_link, back_string = self.get_back()
        context["back"] = back_link
        context["back_string"] = back_string
        context["has_valid_token_in_session"] = self.has_valid_token_in_session(
            self.request
        )
        return context


class ProposalCreateView(idea_views.AbstractIdeaCreateView):
    model = models.Proposal
    form_class = forms.ProposalForm
    permission_required = "meinberlin_budgeting.add_proposal"
    template_name = "meinberlin_budgeting/proposal_create_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ProposalUpdateView(idea_views.AbstractIdeaUpdateView):
    model = models.Proposal
    form_class = forms.ProposalForm
    permission_required = "meinberlin_budgeting.change_proposal"
    template_name = "meinberlin_budgeting/proposal_update_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ProposalDeleteView(idea_views.AbstractIdeaDeleteView):
    model = models.Proposal
    success_message = _("Your budget request has been deleted")
    permission_required = "meinberlin_budgeting.change_proposal"
    template_name = "meinberlin_budgeting/proposal_confirm_delete.html"


class ProposalModerateView(idea_views.AbstractIdeaModerateView):
    model = models.Proposal
    permission_required = "meinberlin_budgeting.moderate_proposal"
    template_name = "meinberlin_budgeting/proposal_moderate_form.html"
    moderateable_form_class = forms.ProposalModerateForm
    remark_form_class = ModeratorRemarkForm


class ProposalDashboardExportView(DashboardExportView):
    template_name = "a4exports/export_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.module.blueprint_type == "PB3":
            context["export"] = reverse(
                "a4dashboard:3-phase-budgeting-export",
                kwargs={"module_slug": self.module.slug},
            )
        elif self.module.blueprint_type in ["PB", "PB2"]:
            if self.module.has_feature("rate", models.Proposal):
                context["export"] = reverse(
                    "a4dashboard:budgeting-export-with-rates",
                    kwargs={"module_slug": self.module.slug},
                )
            else:
                context["export"] = reverse(
                    "a4dashboard:budgeting-export",
                    kwargs={"module_slug": self.module.slug},
                )

        context["comment_export"] = reverse(
            "a4dashboard:budgeting-comment-export",
            kwargs={"module_slug": self.module.slug},
        )
        return context
