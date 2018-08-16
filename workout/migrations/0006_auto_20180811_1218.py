# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-11 09:18
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0005_auto_20180811_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='unit',
            field=models.IntegerField(choices=[(0, 'Kilometers'), (1, 'Reps')], default=1),
        ),
        migrations.AlterField(
            model_name='set',
            name='reps',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(600)]),
        ),
    ]