from django.contrib.auth import models as auth_models
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from . import USERNAME_INVALID_MESSAGE
from . import USERNAME_REGEX


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=60,
        unique=True,
        help_text=_(
            'Required. 60 characters or fewer. Letters, digits, spaces and '
            '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                USERNAME_REGEX, USERNAME_INVALID_MESSAGE, 'invalid')],
        error_messages={
            'unique': _('A user with that username already exists.')}
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _('A user with that email address already exists.')}
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.')
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.')
    )

    date_joined = models.DateTimeField(
        editable=False,
        default=timezone.now
    )

    objects = auth_models.UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_short_name(self):
        return self.username
