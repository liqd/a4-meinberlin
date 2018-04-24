from django.db import models

from adhocracy4.ckeditor.fields import RichTextCollapsibleUploadingField
from adhocracy4.modules import models as module_models


class FaceToFace(module_models.Item):
    title = models.CharField(max_length=120, blank=True)
    text = RichTextCollapsibleUploadingField(
        config_name='collapsible-image-editor'
    )

    def get_absolute_url(self):
        return self.project.get_absolute_url()
