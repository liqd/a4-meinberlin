from django import forms

from . import models


class FaceToFaceForm(forms.ModelForm):

    class Meta:
        model = models.FaceToFace
        fields = ['title', 'text']
