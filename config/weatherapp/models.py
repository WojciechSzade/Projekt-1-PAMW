from jsonfield import JSONField
from django.db import models
import requests

# Create your models here.
class Forecast(models.Model):
    def __init__(self, city_key, days, api_key):
        forecast = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/" + str(days) + "day/" + str(city_key), params={"apikey": str(api_key)})
        if not forecast.ok:
            self.msg = forecast
            return
        forecast = forecast.json()
        self.headline = forecast['Headline']['Text']
        self.minimum_temperature = forecast['DailyForecasts'][0]['Temperature']['Minimum']['Value']
        self.maximum_temperature = forecast['DailyForecasts'][0]['Temperature']['Maximum']['Value']
        self.days = days
        self.city_key = city_key
        self.forecast = forecast
        self.msg = "OK"
        
    headline = models.CharField(max_length=200)
    minimum_temperature = models.FloatField()
    maximum_temperature = models.FloatField()
    days = models.IntegerField()
    city_key = models.IntegerField()
    forecast = JSONField(default=dict)
    msg = models.CharField(max_length=200)
class CityForecast(models.Model):
    name = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    
class CitiesForecast(models.Model):
    def get_data_from_api(self):
        forecast_cities = requests.get("http://dataservice.accuweather.com/currentconditions/v1/topcities/50", params={"apikey": self.api_key})
        if not forecast_cities.ok:
            self.msg = forecast_cities
            return
        forecast_cities = forecast_cities.json()
        for city in forecast_cities:
            c = CityForecast.objects.create(name=city['EnglishName'], text=city['WeatherText'])
            self.cities.add(c)
        self.msg = "OK"
    cities = models.ManyToManyField(CityForecast)
    msg = models.CharField(max_length=200)
    api_key = models.CharField(max_length=200)


class HourForecast(models.Model):
    time = models.DateTimeField()
    weather = models.CharField(max_length=200)
    temperature = models.FloatField()    

class HistoricalForecast(models.Model):
    def get_data_from_api(self):
        forecast = requests.get("http://dataservice.accuweather.com/currentconditions/v1/" + self.city_key + "/historical/24/", params={"apikey": self.api_key})
        if not forecast.ok:
            self.msg = forecast
            return
        forecast = forecast.json()
        for hour in forecast:
            h = HourForecast.objects.create(time=hour['LocalObservationDateTime'], weather=hour['WeatherText'], temperature=hour['Temperature']['Metric']['Value'])
            self.hours.add(h)
        self.msg = "OK"
    
    hours = models.ManyToManyField(HourForecast)
    api_key = models.CharField(max_length=200)
    city_key = models.IntegerField()
    msg = models.CharField(max_length=200)
    
