from django.views import generic
from rules.contrib.views import LoginRequiredMixin


class SearchProfileListView(LoginRequiredMixin, generic.TemplateView):
    template_name = "meinberlin_kiezradar/search_profile_list.html"


class KiezRadarListView(LoginRequiredMixin, generic.TemplateView):
    template_name = "meinberlin_kiezradar/kiezradar_list.html"


class KiezRadarDetailView(LoginRequiredMixin, generic.TemplateView):
    template_name = "meinberlin_kiezradar/kiezradar_detail.html"


class KiezRadarCreateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "meinberlin_kiezradar/kiezradar_create.html"
