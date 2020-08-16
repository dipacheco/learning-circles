# Generated by Django 2.2.13 on 2020-08-04 15:34

from django.db import migrations, models
import django_bleach.models


class Migration(migrations.Migration):

    dependencies = [
        ('studygroups', '0133_announcement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studygroup',
            name='venue_website',
            field=models.URLField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='team',
            name='intro_text',
            field=django_bleach.models.BleachField(blank=True, max_length=1000),
        ),
    ]