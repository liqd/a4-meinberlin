import csv

from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand
from django.db import models

from apps.users.models import User


class Command(BaseCommand):
    help = 'Import users from csv file exported with A3'

    def add_arguments(self, parser):
        parser.add_argument('inputfile', type=str)

    def handle(self, inputfile, *args, **options):
        with open(inputfile) as f:
            reader = csv.DictReader(f, delimiter=';')

            for user in reader:
                self._add_user(user)

    def _add_user(self, userdata):
        email = userdata['Email']
        username = userdata['Username']

        user_exists = User.objects.filter(
            models.Q(email=email) | models.Q(username=username)
        )

        email_exists = EmailAddress.objects.filter(email=email)

        if user_exists or email_exists:
            print('Skipping user {} <{}>'.format(username, email))
        else:
            user = User(
                username=username,
                email=email,
                date_joined=userdata['Creation date'],
                password="bcrypt$" + userdata['Password hash'],
            )
            user.save()
            email = EmailAddress(
                user=user,
                email=userdata['Email'],
                verified=True,
                primary=True,
            )
            email.save()
