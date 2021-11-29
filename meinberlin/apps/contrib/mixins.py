from django import forms
from django.utils.translation import gettext_lazy as _

RIGHT_OF_USE_LABEL = _('I hereby confirm that the copyrights for this '
                       'photo are with me or that I have received '
                       'rights of use from the author. I also confirm '
                       'that the privacy rights of depicted third persons '
                       'are not violated. ')


class DynamicChoicesMixin(object):
    """Dynamic choices mixin.

    Add callable functionality to filters that support the ``choices``
    argument. If the ``choices`` is callable, then it **must** accept the
    ``request`` object as a single argument.

    FIXME: check!
    The ``request`` object may be None if the parent FilterSet is not class
    based.

    This is useful for dymanic ``choices`` determined properties on the
    ``request`` object.

    Like
    https://github.com/carltongibson/django-filter/blob/
    ab7978323ff092c0ccd2b95e9b190ba8522bde11/django_filters/filters.py#L295

    Was changed from request to view in
    https://github.com/liqd/a4-meinberlin/commit/
    ea74f6ad5b04922a7c10477a9074b3047189c8db
    """

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices')
        super().__init__(*args, **kwargs)

    def get_request(self):
        try:
            return self.parent.request
        except AttributeError:
            return None

    def get_choices(self, request):
        choices = self.choices

        if callable(choices):
            return choices(request)
        return choices

    @property
    def field(self):
        request = self.get_request()
        choices = self.get_choices(request)

        if choices is not None:
            self.extra['choices'] = choices

        return super(DynamicChoicesMixin, self).field


class ImageRightOfUseMixin(forms.ModelForm):
    right_of_use = forms.BooleanField(required=False, label=RIGHT_OF_USE_LABEL)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.image:
            self.initial['right_of_use'] = True

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        right_of_use = cleaned_data.get('right_of_use')
        if image and not right_of_use:
            self.add_error('right_of_use',
                           _("You want to upload an image. "
                             "Please check that you have the "
                             "right of use for the image."))
        return cleaned_data


class ContactStorageConsentMixin(forms.ModelForm):

    contact_storage_consent = forms.BooleanField(required=False,
                                                 label=_('contact storage '
                                                         'consent'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.allow_contact and \
           not self.instance.contact_email == '':
            self.initial['contact_storage_consent'] = True

    def clean(self):
        cleaned_data = super().clean()
        allow_contact = cleaned_data.get('allow_contact')
        contact_storage_consent = cleaned_data.get('contact_storage_consent')
        if allow_contact and not contact_storage_consent:
            self.add_error('contact_storage_consent',
                           _('Please consent to the storage of your contact '
                             'information.'))
        return cleaned_data
