from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class IssuePhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'issue'
    weight = 10
    view = views.IdeaListView

    name = _('Issue phase')
    description = _('Create new ideas.')
    module_name = _('ideas collection')

    features = {
        'crud': (models.Idea,),
    }


class CollectPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'collect'
    weight = 20
    view = views.IdeaListView

    name = _('Collect phase')
    description = _('Create and comment new ideas.')
    module_name = _('ideas collection')

    features = {
        'crud': (models.Idea,),
        'comment': (models.Idea,),
    }


class RatingPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'rating'
    weight = 30
    view = views.IdeaListView

    name = _('Rating phase')
    description = _('Get quantative feeback by rating the collected ideas.')
    module_name = _('ideas collection')

    features = {
        'rate': (models.Idea,)
    }


class FeedbackPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'feedback'
    weight = 40
    view = views.IdeaListView

    name = _('Feedback phase')
    description = _('Get feedback for collected ideas through rates and '
                    'comments.')
    module_name = _('ideas collection')

    features = {
        'rate': (models.Idea,),
        'comment': (models.Idea,)
    }


class UniversalPhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'universal'
    weight = 50
    view = views.IdeaListView

    name = _('Universal phase')
    module_name = _('ideas collection')
    description = _('Use all features of the idea collection.')

    features = {
        'crud': (models.Idea,),
        'comment': (models.Idea,),
        'rate': (models.Idea,),
    }


phases.content.register(IssuePhase())
phases.content.register(CollectPhase())
phases.content.register(RatingPhase())
phases.content.register(FeedbackPhase())
phases.content.register(UniversalPhase())
