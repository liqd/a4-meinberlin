import uuid

from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from adhocracy4 import transforms
from adhocracy4.models import base
from adhocracy4.projects.models import Project

from . import emails


class Invite(base.TimeStampedModel):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4, unique=True)

    class Meta:
        abstract = True
        unique_together = ('email', 'project')

    def accept(self, user):
        self.delete()

    def reject(self):
        self.delete()


class ParticipantInviteManager(models.Manager):
    def invite(self, creator, project, email):
        invite = super().create(project=project, creator=creator, email=email)
        emails.InviteParticipantEmail.send(invite)
        return invite


class ParticipantInvite(Invite):

    objects = ParticipantInviteManager()

    def __str__(self):
        return 'Participation invite to {s.project} for {s.email}'.format(
            s=self)

    def get_absolute_url(self):
        url_kwargs = {'invite_token': self.token}
        return reverse('project-participant-invite-detail', kwargs=url_kwargs)

    def accept(self, user):
        self.project.participants.add(user)
        super().accept(user)


class ModeratorInviteManager(models.Manager):
    def invite(self, creator, project, email):
        invite = super().create(project=project, creator=creator, email=email)
        emails.InviteModeratorEmail.send(invite)
        return invite


class ModeratorInvite(Invite):

    objects = ModeratorInviteManager()

    def __str__(self):
        return 'Moderation invite to {s.project} for {s.email}'.format(s=self)

    def get_absolute_url(self):
        url_kwargs = {'invite_token': self.token}
        return reverse('project-moderator-invite-detail', kwargs=url_kwargs)

    def accept(self, user):
        self.project.moderators.add(user)
        super().accept(user)


class ProjectInformationSection(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=255,
        verbose_name=_('Title of the section'),
        help_text=_('This title will appear as the heading of the section. '
                    'It will always be visible and opens the accordion text '
                    'on click.')
    )
    body = RichTextField()
    weight = models.SmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.body = transforms.clean_html_field(self.body)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['weight', 'pk']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.project.get_absolute_url()
