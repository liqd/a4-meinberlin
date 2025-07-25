from django import forms
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from adhocracy4.categories.forms import CategorizableFieldMixin
from adhocracy4.images.validators import ImageAltTextValidator
from adhocracy4.labels.mixins import LabelsAddableFieldMixin
from meinberlin.apps.contrib.mixins import CategoryAndLabelAliasMixin

from . import models


class TopicForm(
    CategorizableFieldMixin,
    LabelsAddableFieldMixin,
    CategoryAndLabelAliasMixin,
    forms.ModelForm,
):
    description = CKEditor5Field(
        config_name="image-editor", validators=[ImageAltTextValidator()]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].label = _("Description")

    class Meta:
        model = models.Topic
        fields = ["name", "description", "category", "labels"]
        help_texts = {
            "description": _(
                "If you add an image, please provide an alternate text. "
                "It serves as a textual description of the image content "
                "and is read out by screen readers. Describe the image "
                "in approx. 80 characters. Example: A busy square with "
                "people in summer."
            ),
        }
