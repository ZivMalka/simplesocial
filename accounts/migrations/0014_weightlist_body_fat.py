# Generated by Django 2.0.5 on 2018-07-22 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20180721_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='weightlist',
            name='body_fat',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
