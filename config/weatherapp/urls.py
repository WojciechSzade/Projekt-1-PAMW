from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cities", views.cities, name="cities"),
    path("oneday/<str:city_key>", views.oneday, name="oneday"),
    path("fiveday/<str:city_key>", views.fiveday, name="fiveday"),
]