# Generated by Django 2.0.5 on 2018-08-12 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20180812_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
