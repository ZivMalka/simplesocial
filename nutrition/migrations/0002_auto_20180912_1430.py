# Generated by Django 2.0.7 on 2018-09-12 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plan',
            options={},
        ),
        migrations.AlterField(
            model_name='plan',
            name='subtitle',
            field=models.CharField(max_length=40),
        ),
    ]