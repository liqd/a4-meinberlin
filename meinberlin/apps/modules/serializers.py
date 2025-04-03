from rest_framework import serializers

from adhocracy4.modules.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id",)
