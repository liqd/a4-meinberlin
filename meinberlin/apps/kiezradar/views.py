from django.views import generic


class SearchProfileListView(generic.TemplateView):
    template_name = "meinberlin_kiezradar/search_profile_list.html"
