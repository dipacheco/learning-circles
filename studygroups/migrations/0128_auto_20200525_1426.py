# Generated by Django 2.2.10 on 2020-05-25 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studygroups', '0127_auto_20200524_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studygroup',
            name='name',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
