from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from adhocracy4 import transforms
from adhocracy4.administrative_districts.models import AdministrativeDistrict
from adhocracy4.images.fields import ConfiguredImageField
from adhocracy4.maps import fields as map_fields
from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.phases.models import Phase
from adhocracy4.projects import models as project_models
from adhocracy4.projects.enums import Access
from adhocracy4.projects.fields import TopicField


class Plan(UserGeneratedContentModel):

    PARTICIPATION_YES = 0
    PARTICIPATION_NO = 1
    PARTICIPATION_UNDECIDED = 2
    PARTICIPATION_CHOICES = (
        (PARTICIPATION_YES, _('with')),
        (PARTICIPATION_NO, _('without')),
        (PARTICIPATION_UNDECIDED, _('undecided')),
    )

    STATUS_ONGOING = 0
    STATUS_DONE = 1

    STATUS_CHOICES = (
        (STATUS_ONGOING, _('running')),
        (STATUS_DONE, _('done'))
    )

    title = models.CharField(
        max_length=120,
        verbose_name=_('Title of your plan'),
        help_text=_('Enter a meaningful title with a maximum '
                    'length of 120 characters. The title'
                    ' will appear in the project tile and on '
                    'top of the plan detail page.')
    )
    organisation = models.ForeignKey(
        settings.A4_ORGANISATIONS_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Organisation'))
    projects = models.ManyToManyField(
        project_models.Project,
        related_name='plans',
        blank=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    point = map_fields.PointField(
        blank=True,
        verbose_name=_('Can your plan be located on the map?'),
        help_text=_('If you locate your plan, it will be shown '
                    'on the map in the project overview in addition '
                    'to the list. To set a pin, click inside the '
                    'highlighted area or enter an address. Once a '
                    'pin is set you can move it by dragging it.')
    )
    point_label = models.CharField(
        blank=True,
        default='',
        max_length=255,
        verbose_name=_('Name of the site'),
        help_text=_('The name of the site (e.g. name of street, '
                    'building or park) makes it easier to locate '
                    'the plan. The maximum length is 255 characters.'),
    )
    district = models.ForeignKey(
        AdministrativeDistrict,
        verbose_name=_('District'),
        help_text=_('Enter the district in which the plan is located or '
                    'whether it is a city-wide plan. In the project '
                    'overview projects can be filtered by district.'),
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    contact_address_text = models.TextField(
        max_length=1000,
        verbose_name=_('Contact for queries'),
        help_text=_('Please name a contact person so users know who '
                    'to contact with any questions they may have.')
    )
    cost = models.CharField(
        max_length=255,
        verbose_name=_('Cost'),
        help_text=_('Enter details of the estimated or actual costs '
                    'of the plan in no more than 255 characters.')
    )
    description = RichTextField(
        verbose_name=_('Description of your plan'),
        help_text=_('Describe the cornerstones of your plan. '
                    'You can upload PDFs and images, embed '
                    'videos and link to external URLs.')
    )
    description_image = ConfiguredImageField(
        'plan_image',
        verbose_name=_('Add image'),
        upload_to='plan/description_image',
        blank=True,
        help_prefix=_(
            'Visualize your plan.'
        ),
    )
    description_image_copyright = models.CharField(
        verbose_name=_('Image copyright'),
        blank=True,
        max_length=120
    )
    topics = TopicField(
        verbose_name=_('Topics'),
        help_text=_('Assign your plan to 1 or 2 '
                    'topics. In the project '
                    'overview projects can be '
                    'filtered according to topics.')
    )
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        verbose_name=_('Status'),
        help_text=_('In the project overview projects '
                    'can be filtered by status.')
    )
    participation = models.SmallIntegerField(
        choices=PARTICIPATION_CHOICES,
        verbose_name=_('Participation'),
        help_text=_('In the project overview '
                    'projects can be filtered '
                    'according to participation '
                    'status.')
    )
    duration = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=_('Duration'),
        help_text=_('Provide information on the '
                    'expected duration of the plan in '
                    'no more than 255 characters.')
    )

    class Meta:
        ordering = ['-created']

    @property
    def reference_number(self):
        return '{:d}-{:05d}'.format(self.created.year, self.pk)

    @property
    def administrative_district(self):
        return self.district

    @property
    def topic_names(self):
        if hasattr(settings, 'A4_PROJECT_TOPICS'):
            choices = dict(settings.A4_PROJECT_TOPICS)
            return [choices.get(topic, topic) for topic in self.topics]
        return []

    @cached_property
    def published_projects(self):
        return self.projects.filter(
            Q(access=Access.PUBLIC) | Q(access=Access.SEMIPUBLIC),
            is_draft=False, is_archived=False)

    @cached_property
    def participation_string(self):
        project_list = self.published_projects.values_list('id', flat=True)
        phases_in_plan = Phase.objects\
            .select_related('module__project')\
            .filter(module__project_id__in=project_list)\
            .order_by('-start_date')

        if phases_in_plan.active_phases():
            return _('running')

        future_phases_with_start_date = phases_in_plan.future_phases()\
            .exclude(start_date__isnull=True)

        if future_phases_with_start_date:
            future_phase = future_phases_with_start_date.first()
            return _('starts at {}')\
                .format(future_phase.start_date.strftime('%d.%m.%Y'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('meinberlin_plans:plan-detail',
                       kwargs=dict(pk='{:05d}'.format(self.pk),
                                   year=self.created.year))

    def save(self, *args, **kwargs):
        self.description = transforms.clean_html_field(self.description)
        super().save(*args, **kwargs)

    def _get_group(self, user, organisation):
        user_groups = user.groups.all()
        org_groups = organisation.groups.all()
        shared_groups = user_groups & org_groups
        return shared_groups.distinct().first()

    def is_group_member(self, user):
        if self.group:
            return user.groups.filter(id=self.group.id).exists()
        return False
