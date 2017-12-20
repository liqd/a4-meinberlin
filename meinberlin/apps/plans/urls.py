from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<reference_number>\d{4}-\d+)/$',
        views.PlanDetailView.as_view(), name='plan-detail'),
    url('^export/format/xslx/$',
        views.PlanExportView.as_view(), name='plan-export'),
    url('^$',
        views.PlanListView.as_view(), name='plan-list'),
]
