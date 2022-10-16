import os
from django.conf import settings
from django.db import models
from django.utils import timezone


def member_directory_path_profile(instance, filename):
    profile_picture_name = 'Members/Profiles/Picture/{0}/profile.jpg'.format(instance)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_picture_name)
    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_picture_name


genders = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
]


class Member(models.Model):
    first_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)
    picture_profile = models.ImageField(upload_to=member_directory_path_profile, blank=True, null=True,
                                        default='anonymous_user.png')
    dni = models.IntegerField(unique=True)
    gender = models.CharField(choices=genders, null=False, max_length=12)
    email = models.EmailField(null=False)
    address = models.CharField(max_length=200, null=False)
    phone_number = models.CharField(max_length=15, null=False)
    birth_date = models.DateField(null=False, blank=False)
    bio = models.TextField(null=True, blank=True, max_length=300)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.dni}_{self.first_name}'

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_profile_picture(self):
        if self.picture_profile:
            return '{}{}'.format(settings.MEDIA_URL, self.picture_profile)
        else:
            return ' '

    def get_age(self):
        current_year = timezone.now().today().year
        return current_year - self.birth_date.year

    def get_short_bio(self):
        if len(self.bio) > 30:
            return self.bio[:30] + '...'
        return self.bio

    def get_gender(self):
        if self.gender == 'M':
            return "<box-icon name='male' ></box-icon>"
        else:
            return "<box-icon name='female' ></box-icon>"

    def get_phone_number(self):
        if self.phone_number.startswith('+'):
            return self.phone_number[1:].replace(' ', '')
        return self.phone_number.replace(' ', '')

    def get_birth_date(self):
        return self.birth_date


allergies = [
    ('Comida', 'Comida'),
    ('Medicamentos', 'Medicamentos'),
    ('Animales', 'Animales'),
    ('Otro', 'Otro'),
    ('Nada', 'Nada'),
]


blood_types = [
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('No lo sé', 'No lo sé'),
]


class MedicalData(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    allergies = models.CharField(choices=allergies, default='Nada', null=False, max_length=15)
    allergies_description = models.CharField(max_length=500, null=True, blank=True)
    blood_type = models.CharField(choices=blood_types, default='No lo sé', max_length=10)
    chronic_disease = models.CharField(max_length=500, null=True, blank=True)
    disease_history = models.CharField(max_length=500, null=True, blank=True)
    treatment_history = models.CharField(max_length=500, null=True, blank=True)
    current_medications = models.CharField(max_length=500, null=True, blank=True)
    comment = models.CharField(max_length=800, null=True, blank=True)

    def __str__(self):
        return self.member.first_name


class AcademicData(models.Model):
    STATUS = [
        ('in_process', 'En proceso'),
        ('culminated', 'Culminado'),
        ('paralyzed', 'Paralizado'),
    ]

    LEVEL = [
        ('preschool', 'Preescolar'),
        ('primary', 'Primaria'),
        ('secondary', 'Secundaria'),
        ('technical', 'Técnico'),
        ('technology', 'Tecnología'),
        ('bachelors_degree', 'Licenciatura'),
        ('postgraduate', 'Posgrado'),
        ('doctorate', 'Doctorado'),
        ('postdoc', 'Postdoctorado'),
    ]

    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    level = models.CharField(max_length=100, null=False, blank=False, choices=LEVEL)
    status = models.CharField(max_length=50, null=False, blank=False, choices=STATUS)
    aspiration = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.member.first_name
