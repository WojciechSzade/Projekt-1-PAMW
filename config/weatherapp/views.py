from django.shortcuts import render
from django.http import HttpResponse
import requests
from decouple import config


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
    forecast = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/1day/" + city_key, params={"apikey": api_key})
    if not forecast.ok:
        return HttpResponse(forecast)
    forecast = forecast.json()
    body = "<html><body>"
    body += "<h1>One Day Forecast</h1>"
    body += "<ul>"
    body += "<li>Headline: " + forecast['Headline']['Text'] + "</li>"
    body += "<li>Minimum Temperature: " + str((forecast)['DailyForecasts'][0]['Temperature']['Minimum']['Value']) + "</li>"
    body += "<li>Maximum Temperature: " + str((forecast)['DailyForecasts'][0]['Temperature']['Maximum']['Value']) + "</li>"
    body += "</ul>"
    body += "</body></html>"
    return HttpResponse(body)


def fiveday(request, city_key):
    forecast = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/5day/" + city_key, params={"apikey": api_key})
    if not forecast.ok:
        return HttpResponse(forecast)
    forecast = forecast.json()
    body = "<html><body>"
    body += "<h1>Five Day Forecast</h1>"
    body += "<ul>"
    body += "<li>Headline: " + forecast['Headline']['Text'] + "</li>"
    body += "<li>Minimum Temperature: " + str(forecast['DailyForecasts'][0]['Temperature']['Minimum']['Value']) + "</li>"
    body += "<li>Maximum Temperature: " + str(forecast['DailyForecasts'][0]['Temperature']['Maximum']['Value']) + "</li>"
    body += "</ul>"
    body += "</body></html>"
    return HttpResponse(body) 

def cities_forecast(request):
    forecast_cities = requests.get("http://dataservice.accuweather.com/currentconditions/v1/topcities/50", params={"apikey": api_key})
    if not forecast_cities.ok:
        return HttpResponse(forecast_cities)
    forecast_cities = forecast_cities.json()
    body = "<html><body> <h1>Top 50 Cities</h1> <ul>"
    for city in forecast_cities:
        body += "<li>" + city['EnglishName'] + ": "
        body += str(city['WeatherText']) + "</br>"
        
    body += "</ul></body></html>"
    
    return HttpResponse(body)


def historical(request, city_key):
    forecast = requests.get("http://dataservice.accuweather.com/currentconditions/v1/" + city_key + "/historical/24/", params={"apikey": api_key})
    if not forecast.ok:
        return HttpResponse(forecast)
    forecast = forecast.json()
    body = "<html><body>"
    body += "<h1>Historical forecast</h1>"
    body += "<ul>"
    for hour in forecast:
        body+= "<li>Time: " + str(hour['LocalObservationDateTime']) + "</li>"
        body+= "<li>Weather: " + str(hour['WeatherText']) + "</li>"
        body+= "<li>Temperature: " + str(hour['Temperature']['Metric']['Value']) + "</li>"
    body += "</ul>"
    body += "</body></html>"
    return HttpResponse(body)

