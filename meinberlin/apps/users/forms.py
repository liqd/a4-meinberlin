import collections

from allauth.account import forms as allauth_forms
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from meinberlin.apps.captcha.fields import CaptcheckCaptchaField
from meinberlin.apps.organisations.models import Organisation
from meinberlin.apps.users.models import User


class UserAdminForm(auth_forms.UserChangeForm):
    def clean(self):
        groups = self.cleaned_data.get("groups")
        group_list = groups.values_list("id", flat=True)
        group_organisations = Organisation.objects.filter(
            groups__in=group_list
        ).values_list("name", flat=True)
        duplicates = [
            item
            for item, count in collections.Counter(group_organisations).items()
            if count > 1
        ]
        if duplicates:
            count = len(duplicates)
            message = ngettext(
                "User is member in more than one group "
                "in this organisation: %(duplicates)s.",
                "User is member in more than one group "
                "in these organisations: %(duplicates)s.",
                count,
            ) % {"duplicates": ", ".join(duplicates)}
            raise ValidationError(message)
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            user = User.objects.get(username__iexact=username)
            if user != self.instance:
                raise forms.ValidationError(
                    User._meta.get_field("username").error_messages["unique"]
                )
        except User.DoesNotExist:
            pass

        try:
            user = User.objects.get(email__iexact=username)
            if user != self.instance:
                raise forms.ValidationError(
                    User._meta.get_field("username").error_messages["used_as_email"]
                )
        except User.DoesNotExist:
            pass

        return username


class AddUserAdminForm(auth_forms.UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data["username"]
        user = User.objects.filter(username__iexact=username)
        if user.exists():
            raise forms.ValidationError(
                User._meta.get_field("username").error_messages["unique"]
            )
        else:
            user = User.objects.filter(email__iexact=username)
            if user.exists():
                raise forms.ValidationError(
                    User._meta.get_field("username").error_messages["used_as_email"]
                )
        return username


class TermsSignupForm(allauth_forms.SignupForm):
    terms_of_use = forms.BooleanField(label=_("Terms of use"))
    get_newsletters = forms.BooleanField(
        label=_("Newsletter"),
        help_text=_(
            "Yes, I would like to receive e-mail newsletters about the projects "
            "I am following. I can undo this at any time in my user "
            "account settings."
        ),
        required=False,
    )
    get_notifications = forms.BooleanField(
        label=_("Notifications"),
        help_text=_(
            "Yes, I would like to be notified by e-mail about the start and "
            "end of participation opportunities. This applies to all projects "
            "I follow. I also receive an e-mail when someone comments on one "
            "of my contributions. I can adapt notification in my user account "
            "settings. "
        ),
        required=False,
        initial=True,
    )
    captcha = CaptcheckCaptchaField(label=_("I am not a robot"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = _(
            "Your username will appear publicly next to your posts."
        )
        self.fields["email"].widget.attrs["autofocus"] = True
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = False
        if not (hasattr(settings, "CAPTCHA_URL") and settings.CAPTCHA_URL):
            del self.fields["captcha"]

    def save(self, request):
        user = super(TermsSignupForm, self).save(request)
        if user:
            user.get_newsletters = self.cleaned_data["get_newsletters"]
            user.get_notifications = self.cleaned_data["get_notifications"]
            user.save()
            return user


class CustomLoginForm(allauth_forms.LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = False
        self.fields["login"].label = _("Username or email")


class CustomResetPasswordForm(allauth_forms.ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = False


class CustomResetPasswordKeyForm(allauth_forms.ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = False


class CustomSetPasswordForm(allauth_forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = False


class CustomChangePasswordForm(allauth_forms.ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = False


class CustomAddEmailForm(allauth_forms.AddEmailForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = False


class SocialTermsSignupForm(SocialSignupForm):
    terms_of_use = forms.BooleanField(label=_("Terms of use"))
    get_newsletters = forms.BooleanField(
        label=_("Newsletter"),
        help_text=_(
            "Yes, I would like to receive e-mail newsletters about "
            "the projects I am following."
        ),
        required=False,
    )
    get_notifications = forms.BooleanField(
        label=_("Notifications"),
        help_text=_(
            "Yes, I would like to be notified by e-mail about the "
            "start and end of participation opportunities. This "
            "applies to all projects I follow. I also receive an "
            "e-mail when someone comments on one of my "
            "contributions."
        ),
        required=False,
        initial=True,
    )
    email = forms.EmailField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = _(
            "Your username will appear publicly next to your posts."
        )

    def save(self, request):
        user = super(SocialTermsSignupForm, self).save(request)
        user.get_newsletters = self.cleaned_data["get_newsletters"]
        user.get_notifications = self.cleaned_data["get_notifications"]
        user.save()
        return user
