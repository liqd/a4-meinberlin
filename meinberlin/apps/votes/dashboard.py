from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components

from . import views


class VotesComponent(DashboardComponent):
    identifier = 'voting_token_export'
    weight = 49
    label = _('Voting codes')

    def is_effective(self, module):
        # FIXME with story module types: make sure only shown in 3 phase
        module_app = module.phases[0].content().app
        return (module_app == 'meinberlin_budgeting' and
                not module.project.is_draft and not module.is_draft)

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse('a4dashboard:voting-tokens', kwargs={
            'module_slug': module.slug,
        })

    def get_urls(self):
        return [
            (r'^modules/(?P<module_slug>[-\w_]+)/voting/$',
             views.VotingDashboardView.as_view(),
             'voting-tokens'),
            (r'^modules/(?P<module_slug>[-\w_]+)/voting/export-token/$',
             views.TokenExportView.as_view(),
             'token-export'),
        ]


components.register_module(VotesComponent())
