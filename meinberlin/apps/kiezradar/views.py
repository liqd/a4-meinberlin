from django.views import generic
from rules.contrib.views import LoginRequiredMixin


class SearchProfileListView(LoginRequiredMixin, generic.TemplateView):
    template_name = "meinberlin_kiezradar/search_profile_list.html"


class KiezRadarView(LoginRequiredMixin, generic.TemplateView):
    template_name = "meinberlin_kiezradar/kiezradar.html"
