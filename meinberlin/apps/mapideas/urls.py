from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<year>\d{4})-(?P<pk>\d+)/$',
        views.MapIdeaDetailView.as_view(), name='mapidea-detail'),
    url(r'create/module/(?P<module_slug>[-\w_]+)/$',
        views.MapIdeaCreateView.as_view(), name='mapidea-create'),
    url(r'^(?P<year>\d{4})-(?P<pk>\d+)/update/$',
        views.MapIdeaUpdateView.as_view(), name='mapidea-update'),
    url(r'^(?P<year>\d{4})-(?P<pk>\d+)/delete/$',
        views.MapIdeaDeleteView.as_view(), name='mapidea-delete'),
]
