# Generated by Django 4.2.6 on 2023-11-02 17:18

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=200)),
                ('minimum_temperature', models.FloatField()),
                ('maximum_temperature', models.FloatField()),
                ('days', models.IntegerField()),
                ('city_key', models.IntegerField()),
                ('forecast', jsonfield.fields.JSONField(default=dict)),
                ('msg', models.CharField(max_length=200)),
            ],
        ),
    ]
