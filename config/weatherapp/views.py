from django.shortcuts import render
from django.http import HttpResponse
import requests
from decouple import config


api_key = config('API_KEY')

# Create your views here.
def index(request):
    return HttpResponse("<a href='cities'>Cities</a><a href='minute'>Minute</a>")

def cities(request):
    # api call
    cities = requests.get("http://dataservice.accuweather.com/locations/v1/topcities/50", params={"apikey": api_key})
    cities = cities.json()
    body = "<html><body> <h1>Top 50 Cities</h1> <ul>"
    for city in cities:
        body += "<li>" + city['EnglishName']
        body += ": <a href='/oneday/" + city['Key'] + "'>One Day Forecast</a>"
        body += ": <a href='/fiveday/" + city['Key'] + "'>Five Day Forecast</a>"
        body += "</li>"
    
    body += "</ul></body></html>"
    
    return HttpResponse(body)

def oneday(request, city_key):
    forecast = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/1day/" + city_key, params={"apikey": api_key})
    body = "<html><body>"
    body += "<h1>One Day Forecast</h1>"
    body += "<ul>"
    body += "<li>Headline: " + forecast.json()['Headline']['Text'] + "</li>"
    body += "<li>Minimum Temperature: " + str(forecast.json()['DailyForecasts'][0]['Temperature']['Minimum']['Value']) + "</li>"
    body += "<li>Maximum Temperature: " + str(forecast.json()['DailyForecasts'][0]['Temperature']['Maximum']['Value']) + "</li>"
    body += "</ul>"
    body += "</body></html>"
    return HttpResponse(body)


def fiveday(request, city_key):
    forecast = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/5day/" + city_key, params={"apikey": api_key})
    body = "<html><body>"
    body += "<h1>Five Day Forecast</h1>"
    body += "<ul>"
    body += "<li>Headline: " + forecast.json()['Headline']['Text'] + "</li>"
    body += "<li>Minimum Temperature: " + str(forecast.json()['DailyForecasts'][0]['Temperature']['Minimum']['Value']) + "</li>"
    body += "<li>Maximum Temperature: " + str(forecast.json()['DailyForecasts'][0]['Temperature']['Maximum']['Value']) + "</li>"
    body += "</ul>"
    body += "</body></html>"
    return HttpResponse(body) 