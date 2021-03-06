# Generated by Django 2.2.13 on 2020-07-23 04:30

from django.db import migrations
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('studygroups', '0133_announcement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studygroup',
            name='course_description',
            field=django_bleach.models.BleachField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='studygroup',
            name='description',
            field=django_bleach.models.BleachField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='team',
            name='intro_text',
            field=django_bleach.models.BleachField(blank=True, max_length=1000),
        ),
    ]
