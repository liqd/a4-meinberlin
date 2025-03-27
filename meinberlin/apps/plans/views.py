import json

from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from rest_framework.renderers import JSONRenderer

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.dashboard import mixins as a4dashboard_mixins
from adhocracy4.filters import views as filter_views
from adhocracy4.filters import widgets as filter_widgets
from adhocracy4.filters.filters import DefaultsFilterSet
from adhocracy4.filters.filters import FreeTextFilter
from adhocracy4.projects.models import Topic
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib.enums import TopicEnum
from meinberlin.apps.contrib.views import CanonicalURLDetailView
from meinberlin.apps.dashboard.mixins import DashboardProjectListGroupMixin
from meinberlin.apps.kiezradar.models import KiezRadar
from meinberlin.apps.kiezradar.models import ProjectStatus
from meinberlin.apps.kiezradar.models import ProjectType
from meinberlin.apps.kiezradar.models import SearchProfile
from meinberlin.apps.kiezradar.serializers import KiezRadarSerializer
from meinberlin.apps.kiezradar.serializers import SearchProfileSerializer
from meinberlin.apps.maps.models import MapPreset
from meinberlin.apps.organisations.models import Organisation
from meinberlin.apps.plans import models
from meinberlin.apps.plans import signals
from meinberlin.apps.plans.forms import PlanForm
from meinberlin.apps.plans.models import Plan
from meinberlin.apps.projects.serializers import ProjectSerializer


class FreeTextFilterWidget(filter_widgets.FreeTextFilterWidget):
    label = _("Search")


class PlanFilterSet(DefaultsFilterSet):
    defaults = {}

    search = FreeTextFilter(widget=FreeTextFilterWidget, fields=["title"])

    class Meta:
        model = models.Plan
        fields = ["search"]


class PlanDetailView(rules_mixins.PermissionRequiredMixin, CanonicalURLDetailView):
    model = models.Plan
    template_name = "meinberlin_plans/plan_detail.html"
    permission_required = "meinberlin_plans.view_plan"

    def get_topics(self):
        topics = [
            {
                "id": topic.id,
                "code": topic.code,
                "name": str(TopicEnum(topic.code).label),
            }
            for topic in Topic.objects.all()
        ]
        return json.dumps(topics)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["published_projects"] = json.dumps(
            ProjectSerializer(
                self.object.published_projects, many=True, now=timezone.now()
            ).data
        )
        context["topic_choices"] = self.get_topics()
        context["polygon"] = settings.BERLIN_POLYGON
        return context


class PlanListView(rules_mixins.PermissionRequiredMixin, generic.ListView):
    model = models.Plan
    template_name = "meinberlin_plans/plan_list.html"
    permission_required = "meinberlin_plans.list_plan"

    def get_queryset(self):
        return super().get_queryset().select_related()

    @cached_property
    def districts(self):
        try:
            return MapPreset.objects.filter(category__name="Bezirke - Berlin")
        except ObjectDoesNotExist:
            return []

    def get_organisations(self):
        organisations = Organisation.objects.values("id", "name").order_by("name")
        return json.dumps(list(organisations))

    def get_districts(self):
        districts = AdministrativeDistrict.objects.values("id", "name")
        districts_list = [district for district in districts]
        return json.dumps(districts_list)

    def get_topics(self):
        topics = [
            {
                "id": topic.id,
                "code": topic.code,
                "name": str(TopicEnum(topic.code).label),
            }
            for topic in Topic.objects.all()
        ]
        return json.dumps(topics)

    def get_participation_choices(self):
        project_types = [
            {
                "id": project_type.id,
                "name": project_type.get_participation_display(),
                "value": project_type.participation,
            }
            for project_type in ProjectType.objects.all()
        ]
        return json.dumps(project_types)

    def get_project_status(self):
        statuses = [
            {
                "id": project_status.id,
                "status": project_status.status,
                "name": project_status.get_status_display(),
            }
            for project_status in ProjectStatus.objects.all()
        ]
        return json.dumps(statuses)

    def get_kiezradars(self):
        if not self.request.user.is_authenticated:
            return json.dumps([])

        kiezradars = KiezRadar.objects.filter(creator=self.request.user)
        return (
            JSONRenderer()
            .render(KiezRadarSerializer(kiezradars, many=True).data)
            .decode("utf-8")
        )

    def get_search_profile(self):
        if (
            self.request.GET.get("search-profile", None)
            and self.request.user.is_authenticated
        ):
            search_profile_id = self.request.GET.get("search-profile")
            try:
                search_profile = SearchProfile.objects.get(
                    id=search_profile_id, creator=self.request.user
                )
                return (
                    JSONRenderer()
                    .render(SearchProfileSerializer(instance=search_profile).data)
                    .decode("utf-8")
                )
            except SearchProfile.DoesNotExist:
                pass
        return None

    def get_search_profiles_count(self):
        if self.request.user.is_authenticated:
            return SearchProfile.objects.filter(creator=self.request.user).count()
        else:
            return 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        use_vector_map = 0
        mapbox_token = ""
        omt_token = ""

        if hasattr(settings, "A4_USE_VECTORMAP") and settings.A4_USE_VECTORMAP:
            use_vector_map = 1

        if hasattr(settings, "A4_MAPBOX_TOKEN"):
            mapbox_token = settings.A4_MAPBOX_TOKEN

        if hasattr(settings, "A4_OPENMAPTILES_TOKEN"):
            omt_token = settings.A4_OPENMAPTILES_TOKEN

        context["kiezradars"] = self.get_kiezradars()
        context["search_profile"] = self.get_search_profile()
        context["districts"] = self.get_districts()
        context["organisations"] = self.get_organisations()
        context["topic_choices"] = self.get_topics()
        context["extprojects_api_url"] = reverse("extprojects-list")
        context["privateprojects_api_url"] = reverse("privateprojects-list")
        context["projects_api_url"] = reverse("projects-list")
        context["plans_api_url"] = reverse("plans-list")
        context["baseurl"] = settings.A4_MAP_BASEURL
        context["mapbox_token"] = mapbox_token
        context["omt_token"] = omt_token
        context["use_vector_map"] = use_vector_map
        attribution = ""
        if hasattr(settings, "A4_MAP_ATTRIBUTION"):
            attribution = settings.A4_MAP_ATTRIBUTION
        context["attribution"] = attribution
        context["bounds"] = json.dumps(settings.A4_MAP_BOUNDING_BOX)
        context["district"] = self.request.GET.get("district", -1)
        context["topic"] = self.request.GET.get("topic", -1)
        context["participation_choices"] = self.get_participation_choices()
        context["search_profiles_api_url"] = reverse("searchprofiles-list")
        context["search_profiles_url"] = reverse("search_profiles")
        context["search_profiles_count"] = self.get_search_profiles_count()
        context["is_authenticated"] = json.dumps(self.request.user.is_authenticated)
        context["project_status"] = self.get_project_status()

        return context


class DashboardPlanListView(
    a4dashboard_mixins.DashboardBaseMixin,
    DashboardProjectListGroupMixin,
    filter_views.FilteredListView,
):
    model = Plan
    paginate_by = 12
    template_name = "meinberlin_plans/plan_dashboard_list.html"
    permission_required = "meinberlin_plans.add_plan"
    menu_item = "project"
    filter_set = PlanFilterSet

    def get_permission_object(self):
        return self.organisation

    def get_queryset(self):
        return super().get_queryset().filter(organisation=self.organisation)


class DashboardPlanCreateView(
    a4dashboard_mixins.DashboardBaseMixin, SuccessMessageMixin, generic.CreateView
):
    model = Plan
    form_class = PlanForm
    permission_required = "meinberlin_plans.add_plan"
    template_name = "meinberlin_plans/plan_create_dashboard.html"
    menu_item = "project"
    success_message = _("The plan was created")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.organisation = self.organisation
        return super().form_valid(form)

    def get_permission_object(self):
        return self.organisation

    def get_success_url(self):
        return reverse(
            "a4dashboard:plan-update",
            kwargs={"organisation_slug": self.organisation.slug, "pk": self.object.pk},
        )


class DashboardPlanUpdateView(
    a4dashboard_mixins.DashboardBaseMixin, SuccessMessageMixin, generic.UpdateView
):
    model = Plan
    form_class = PlanForm
    permission_required = "meinberlin_plans.change_plan"
    template_name = "meinberlin_plans/plan_update_form.html"
    menu_item = "project"
    success_message = _("The plan has been updated")

    def get_permission_object(self):
        return self.get_object()


class DashboardPlanDeleteView(
    a4dashboard_mixins.DashboardBaseMixin, generic.DeleteView
):
    model = Plan
    success_message = _("The plan has been deleted")
    permission_required = "meinberlin_plans.change_plan"
    template_name = "meinberlin_plans/plan_confirm_delete.html"
    menu_item = "project"

    def form_valid(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().form_valid(request, *args, **kwargs)

    def get_permission_object(self):
        return self.get_object()

    def get_success_url(self):
        return reverse(
            "a4dashboard:plan-list",
            kwargs={"organisation_slug": self.organisation.slug},
        )


class PlanPublishView(
    SingleObjectMixin, rules_mixins.PermissionRequiredMixin, generic.View
):
    permission_required = "meinberlin_plans.change_plan"
    model = Plan

    def get_permission_object(self):
        return self.get_object()

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", None)
        if action == "publish":
            self.publish_plan()
        elif action == "unpublish":
            self.unpublish_plan()
        else:
            messages.warning(self.request, _("Invalid action"))

        return HttpResponseRedirect(
            reverse(
                "a4dashboard:plan-update",
                kwargs={
                    "organisation_slug": self.get_object().organisation.slug,
                    "pk": self.get_object().pk,
                },
            )
        )

    def publish_plan(self):
        plan = self.get_object()
        if not plan.is_draft:
            messages.info(self.request, _("The plan is already published"))
            return

        plan.is_draft = False
        plan.save()

        signals.plan_published.send(sender=None, plan=plan, user=self.request.user)

        messages.success(self.request, _("The plan is published."))

    def unpublish_plan(self):
        plan = self.get_object()
        if plan.is_draft:
            messages.info(self.request, _("The plan is already unpublished"))
            return

        plan.is_draft = True
        plan.save()

        messages.success(self.request, _("The plan is unpublished."))
