# Generated by Django 4.2.6 on 2023-11-08 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0002_citiesforecast_cityforecast'),
    ]

    operations = [
        migrations.AddField(
            model_name='citiesforecast',
            name='msg',
            field=models.CharField(default='OK', max_length=200),
            preserve_default=False,
        ),
    ]