from django.utils.translation import gettext_lazy as _

default_app_config = 'meinberlin.apps.users.apps.Config'

USERNAME_REGEX = r'^[\w]+[ \w.@+-]*$'
USERNAME_INVALID_MESSAGE = _('Enter a valid username. This value may contain '
                             'only letters, digits, spaces and @/./+/-/_ '
                             'characters. It must start with a digit or a '
                             'letter.')
