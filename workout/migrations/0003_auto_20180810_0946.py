# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-10 06:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0002_auto_20180809_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='day',
            field=models.CharField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], max_length=15),
        ),
    ]