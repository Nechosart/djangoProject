from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hi', views.hi, name='hi'),
    path('hello', views.hello, name='hello')
]