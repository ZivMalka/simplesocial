# Generated by Django 2.0.7 on 2018-09-08 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='goal',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
