# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-17 09:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studygroups', '0093_application_mobile_opt_out_at'),
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearnerSurveyResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeform_key', models.CharField(max_length=64, unique=True)),
                ('survey', models.TextField()),
                ('response', models.TextField()),
                ('responded_at', models.DateTimeField()),
                ('learner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='studygroups.Application')),
                ('study_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='studygroups.StudyGroup')),
            ],
        ),
    ]