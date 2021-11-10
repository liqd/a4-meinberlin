from rest_framework import serializers

from adhocracy4.categories.models import Category

from .models import Proposal


class CategoryField(serializers.Field):

    def to_internal_value(self, category):
        if category:
            return Category.objects.get(pk=category)
        else:
            return None

    def to_representation(self, category):
        return {'id': category.pk, 'name': category.name}


class ProposalSerializer(serializers.ModelSerializer):

    creator = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    positive_rating_count = serializers.SerializerMethodField()
    negative_rating_count = serializers.SerializerMethodField()
    category = CategoryField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Proposal
        fields = ('budget', 'category', 'comment_count', 'created', 'creator',
                  'is_archived', 'name', 'negative_rating_count',
                  'positive_rating_count', 'url')
        read_only_fields = ('budget', 'category', 'comment_count', 'created',
                            'creator', 'is_archived', 'name',
                            'negative_rating_count', 'positive_rating_count',
                            'url')

    def get_creator(self, proposal):
        return proposal.creator.username

    def get_comment_count(self, proposal):
        if hasattr(proposal, 'comment_count'):
            return proposal.comment_count
        else:
            return 0

    def get_positive_rating_count(self, proposal):
        if hasattr(proposal, 'positive_rating_count'):
            return proposal.positive_rating_count
        else:
            return 0

    def get_negative_rating_count(self, proposal):
        if hasattr(proposal, 'negative_rating_count'):
            return proposal.negative_rating_count
        else:
            return 0

    def get_url(self, proposal):
        return proposal.get_absolute_url()
