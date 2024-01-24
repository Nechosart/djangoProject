from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, template_name='home.html')


def hi(request):
    return HttpResponse('Hi')


def hello(request):
    return HttpResponse('Hello')
