# Generated by Django 4.1.1 on 2022-09-26 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Members', '0005_alter_medicaldata_allergies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='dni',
            field=models.IntegerField(unique=True),
        ),
    ]
