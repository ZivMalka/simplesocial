# Generated by Django 2.0.7 on 2018-09-15 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='banner'),
        ),
    ]