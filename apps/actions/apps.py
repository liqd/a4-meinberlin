from django.apps import AppConfig


class Config(AppConfig):
    name = 'apps.actions'
    label = 'meinberlin_actions'

    def ready(self):
        from adhocracy4.actions.models import configure_icon
        from adhocracy4.actions.models import configure_type
        from adhocracy4.actions.verbs import Verbs
        configure_type(
            'project',
            ('a4projects', 'project'),
            ('meinberlin_bplan', 'bplan'),
            ('meinberlin_externalproject', 'externalproject')
        )
        configure_type(
            'phase',
            ('a4phases', 'phase')
        )
        configure_type(
            'comment',
            ('a4comments', 'comment')
        )
        configure_type(
            'rating',
            ('a4ratings', 'rating')
        )
        configure_type(
            'item',
            ('meinberlin_budgeting', 'proposal'),
            ('meinberlin_ideas', 'idea'),
            ('meinberlin_kiezkasse', 'proposal'),
            ('meinberlin_mapideas', 'mapidea')
        )

        configure_icon('comment', type='comment')
        configure_icon('lightbulb-o', type='item')
        configure_icon('plus', verb=Verbs.ADD)
        configure_icon('pencil', verb=Verbs.UPDATE)
        configure_icon('flag', verb=Verbs.START)
        configure_icon('clock-o', verb=Verbs.SCHEDULE)
