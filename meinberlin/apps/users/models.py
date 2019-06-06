from django.contrib.auth import models as auth_models
from django.core import validators
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from meinberlin.apps.organisations.models import Organisation

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
        _('Email address'),
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

    get_notifications = models.BooleanField(
        verbose_name=_('Send me email notifications'),
        default=True,
        help_text=_(
            'Designates whether you want to receive notifications about '
            'content you follow. '
            'Unselect if you do not want to receive notifications.')
    )

    get_newsletters = models.BooleanField(
        verbose_name=_('Send me newsletters'),
        default=False,
        help_text=_(
            'Designates whether you want to receive newsletters. '
            'Unselect if you do not want to receive newsletters.')
    )

    objects = auth_models.UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def organisations(self):
        initiator_orgs = self.organisation_set.all()
        if self.groups.all():
            user_groups = self.groups.all().values_list('id', flat=True)
            group_orgs = Organisation.objects \
                .filter(groups__in=user_groups)
            orgs = initiator_orgs | group_orgs
            return orgs.distinct()
        return initiator_orgs

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        full_name = '%s <%s>' % (self.username, self.email)
        return full_name.strip()

    def signup(self, username, email, commit=True):
        """Update the fields required for sign-up."""
        self.username = username
        self.email = email
        if commit:
            self.save()

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.username)])
