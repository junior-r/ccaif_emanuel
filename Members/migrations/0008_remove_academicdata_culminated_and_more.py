# Generated by Django 4.1.1 on 2022-10-03 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Members', '0007_academicdata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='academicdata',
            name='culminated',
        ),
        migrations.RemoveField(
            model_name='academicdata',
            name='in_process',
        ),
        migrations.RemoveField(
            model_name='academicdata',
            name='paralyzed',
        ),
        migrations.AddField(
            model_name='academicdata',
            name='level',
            field=models.CharField(default='level', max_length=50),
            preserve_default=False,
        ),
    ]
