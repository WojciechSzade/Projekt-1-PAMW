# Generated by Django 4.2.6 on 2023-11-08 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0006_alter_citiesforecast_cities'),
    ]

    operations = [
        migrations.CreateModel(
            name='HourForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('weather', models.CharField(max_length=200)),
                ('temperature', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(max_length=200)),
                ('city_key', models.IntegerField()),
                ('hours', models.ManyToManyField(to='weatherapp.hourforecast')),
            ],
        ),
    ]
