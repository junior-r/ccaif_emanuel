import os
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save


def user_directory_path_profile(instance, filename):
    profile_picture_name = 'Users/Profiles/Picture/{0}/profile.jpg'.format(instance.username)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name


genders = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
]


class User(AbstractUser):
    picture_profile = models.ImageField(upload_to=user_directory_path_profile, blank=True, null=True,
                                        default='anonymous_user.png')
    gender = models.CharField(choices=genders, default='M', null=True, max_length=12)
    dni = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True, max_length=300)

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return self.username

    def __str__(self):
        return self.username
