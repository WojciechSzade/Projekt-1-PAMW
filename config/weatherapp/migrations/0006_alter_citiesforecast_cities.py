# Generated by Django 4.2.6 on 2023-11-08 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0005_citiesforecast_api_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citiesforecast',
            name='cities',
            field=models.ManyToManyField(to='weatherapp.cityforecast'),
        ),
    ]