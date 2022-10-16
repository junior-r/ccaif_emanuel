import os
from django.conf import settings
from django.db import models
from django.utils import timezone
from Users.models import User


def event_directory_path_image(instance, filename):
    image_name = 'Event/Picture/{0}/event.jpg'.format(instance)
    full_path = os.path.join(settings.MEDIA_ROOT, image_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return image_name


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=event_directory_path_image, blank=False, null=False)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=800)
    place = models.CharField(max_length=200)
    date = models.DateField(null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    form = models.BooleanField(default=False)
    max_num_partp = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def get_short_description(self):
        if len(self.description) > 30:
            return self.description[:30] + '...'
        return self.description

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        else:
            return ' '

    def __str__(self):
        return f'{self.title}_{self.date}'

    class Meta:
        ordering = ['date']


class EventParticipant(models.Model):
    event = models.ManyToManyField(Event)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=250)
    birth_date = models.DateField(null=False, blank=False)
    is_member = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_age(self):
        return timezone.now().year - self.birth_date.year
