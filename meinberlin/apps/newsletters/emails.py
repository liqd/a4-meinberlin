from email.mime.image import MIMEImage

from django.apps import apps
from django.conf import settings
from django.contrib import auth

from adhocracy4.emails.mixins import ReportToAdminEmailMixin
from meinberlin.apps.contrib.emails import Email

Organisation = apps.get_model(settings.A4_ORGANISATIONS_MODEL)
User = auth.get_user_model()


class NewsletterEmail(ReportToAdminEmailMixin, Email):
    template_name = 'meinberlin_newsletters/emails/newsletter_email'

    def dispatch(self, object, *args, **kwargs):
        organisation_pk = kwargs.pop('organisation_pk', None)
        organisation = None
        if organisation_pk:
            organisation = Organisation.objects.get(pk=organisation_pk)
        kwargs['organisation'] = organisation

        return super().dispatch(object, *args, **kwargs)

    def get_reply_to(self):
        return ['{} <{}>'.format(self.object.sender_name, self.object.sender)]

    def get_receivers(self):
        return User.objects\
            .filter(id__in=self.kwargs['participant_ids'])\
            .filter(get_newsletters=True)\
            .filter(is_active=True)\
            .distinct()

    def get_attachments(self):
        attachments = super().get_attachments()

        organisation = self.kwargs['organisation']
        if organisation and organisation.logo:
            f = open(organisation.logo.path, 'rb')
            logo = MIMEImage(f.read())
            logo.add_header('Content-ID', '<{}>'.format('organisation_logo'))
            attachments += [logo]

        return attachments


class NewsletterEmailAll(NewsletterEmail):

    def get_receivers(self):
        return User.objects\
            .filter(get_newsletters=True)\
            .filter(is_active=True)\
            .distinct()
