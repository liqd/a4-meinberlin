from django.views import generic
from rules.contrib.views import LoginRequiredMixin


class SearchProfileListView(LoginRequiredMixin, generic.TemplateView):
    template_name = "meinberlin_kiezradar/search_profile_list.html"


# class PlanDetailView(rules_mixins.PermissionRequiredMixin, CanonicalURLDetailView):
#    model = models.Plan
#    template_name = "meinberlin_plans/plan_detail.html"
#    permission_required = "meinberlin_plans.view_plan"


class KiezRadarListView(LoginRequiredMixin, generic.TemplateView):
    template_name = "meinberlin_kiezradar/kiezradar_list.html"


class KiezRadarDetailView(LoginRequiredMixin, generic.TemplateView):
    template_name = "meinberlin_kiezradar/kiezradar_detail.html"


class KiezRadarCreateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "meinberlin_kiezradar/kiezradar_create.html"
