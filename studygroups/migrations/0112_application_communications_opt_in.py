# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-15 12:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studygroups', '0111_auto_20190312_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='communications_opt_in',
            field=models.BooleanField(default=False),
        ),
    ]
