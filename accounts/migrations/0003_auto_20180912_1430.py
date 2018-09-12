# Generated by Django 2.0.7 on 2018-09-12 11:30

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofileinfo_goal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='birth_date',
            field=models.DateField(blank=True, null=True, validators=[accounts.models.birth_date_validation]),
        ),
    ]
