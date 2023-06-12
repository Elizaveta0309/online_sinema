import uuid

from django.db import models
from tinymce.models import HTMLField


class UUIDMixin(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:

        abstract = True


class Channel(models.TextChoices):

    email = 'email'
    websocket = 'websocket'


class UserGroup(models.TextChoices):

    all = 'all'


class Frequency(models.TextChoices):

    once = 'once'
    daily = 'daily'
    weekly = 'weekly'
    monthly = 'monthly'


class Priority(models.TextChoices):

    low = 'low'
    high = 'high'


class Event(models.TextChoices):

    review_rated = 'review-reporting.v1.rated'
    user_registered = 'user-reporting.v1.registered'
    admin = 'admin-reporting.v1.event'


class Template(UUIDMixin):

    name = models.CharField('name', max_length=255)
    description = models.TextField('description', blank=True)
    channel = models.CharField(
        choices=Channel.choices,
        max_length=50,
    )
    subject = models.TextField(blank=True)
    template = HTMLField()
    event = models.CharField(
        choices=Event.choices,
        max_length=50,
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ScheduleMail(UUIDMixin):

    name = models.CharField('name', max_length=255)
    description = models.TextField('description', blank=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    template_params = models.TextField(
        'template_params',
        blank=True,
    )
    user_group = models.CharField(
        choices=UserGroup.choices,
        max_length=50,
    )
    is_instant = models.BooleanField()
    next_planned = models.DateTimeField(blank=True, null=True)
    frequency = models.CharField(
        choices=Frequency.choices,
        max_length=50,
    )
    priority = models.CharField(
        choices=Priority.choices,
        max_length=50,
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    last_processed_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Config(UUIDMixin):

    name = models.SlugField('name', max_length=255)
    config_value = models.CharField('value', max_length=255)
    description = models.TextField('description', blank=True)
