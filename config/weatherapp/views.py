from django.shortcuts import render
from django.http import HttpResponse
import requests
from decouple import config
from .models import *


api_key = config('API_KEY')

# Create your views here.
def index(request):
    return HttpResponse("<a href='cities'>Cities</a></br><a href='cities_forecast'>Cities current conditions</a>")

def cities(request):
    cities = requests.get("http://dataservice.accuweather.com/locations/v1/topcities/50", params={"apikey": api_key})
    if not cities.ok:
        return HttpResponse(cities)
    cities = cities.json()
    body = "<html><body> <h1>Top 50 Cities</h1> <ul>"
    for city in cities:
        body += "<li>" + city['EnglishName']
        body += "; <a href='/oneday/" + city['Key'] + "'>One Day Forecast</a>"
        body += "; <a href='/fiveday/" + city['Key'] + "'>Five Day Forecast</a>"
        body += "; <a href='/historical/" + city['Key'] + "'>Historical 24h Forecast</a>"
        body += "</li>"
    
    body += "</ul></body></html>"
    
    return HttpResponse(body)

def oneday(request, city_key):
    forecast = Forecast(city_key=city_key, days=1, api_key=api_key)
    if forecast.msg != "OK":
        return HttpResponse(forecast.msg)
    body = "<html><body>"
    body += "<h1>One Day Forecast</h1>"
    body += "<ul>"
    body += "<li>Headline: " + str(forecast.headline) + "</li>"
    body += "<li>Minimum Temperature: " + str(forecast.minimum_temperature) + "</li>"
    body += "<li>Maximum Temperature: " + str(forecast.maximum_temperature) + "</li>"
    body += "</ul>"
    body += "</body></html>"
    return HttpResponse(body)


def fiveday(request, city_key):
    forecast = Forecast(city_key=city_key, days=5, api_key=api_key)
    if forecast.msg != "OK":
        return HttpResponse(forecast.msg)
    body = "<html><body>"
    body += "<h1>Five Day Forecast</h1>"
    body += "<ul>"
    body += "<li>Headline: " + str(forecast.headline) + "</li>"
    body += "<li>Minimum Temperature: " + str(forecast.minimum_temperature) + "</li>"
    body += "<li>Maximum Temperature: " + str(forecast.maximum_temperature) + "</li>"
    body += "</ul>"
    body += "</body></html>"
    return HttpResponse(body) 

def cities_forecast(request):
    forecast_cities = CitiesForecast.objects.create(api_key=api_key)
    forecast_cities.get_data_from_api()
    if forecast_cities.msg != "OK":
        return HttpResponse(forecast_cities.msg)
    body = "<html><body> <h1>Top 50 Cities</h1> <ul>"
    for city in forecast_cities.cities.all():
        body += "<li>" + city.name + ": "
        body += str(city.text) + "</br>"
        
    body += "</ul></body></html>"
    
    return HttpResponse(body)


def historical(request, city_key):
    forecast = HistoricalForecast.objects.create(city_key=city_key, api_key=api_key)
    forecast.get_data_from_api()
    if not forecast.msg == "OK":
        return HttpResponse(forecast)
    body = "<html><body>"
    body += "<h1>Historical forecast</h1>"
    body += "<ul>"
    for hour in forecast.hours.all():
        body+= "<li>Time: " + str(hour.time) + "</li>"
        body+= "<li>Weather: " + str(hour.weather) + "</li>"
        body+= "<li>Temperature: " + str(hour.temperature) + "</li>"
    body += "</ul>"
    body += "</body></html>"
    return HttpResponse(body)

