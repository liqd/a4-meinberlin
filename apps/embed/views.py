from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.clickjacking import xframe_options_exempt


class EmbedView(generic.base.TemplateView):
    @xframe_options_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class EmbedProjectView(EmbedView):
    template_name = "meinberlin_embed/embed.html"

    @xframe_options_exempt
    def dispatch(self, request, *args, **kwargs):
        default = reverse('project-detail', args=[self.kwargs['slug']])
        self.initial_url = request.GET.get('initialUrl', default)
        return super().dispatch(request, *args, **kwargs)
