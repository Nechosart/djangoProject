from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=32)


class Product(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    changed_date = models.DateTimeField(auto_now=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Artist(models.Model):
    name = models.CharField(max_length=64)
    year = models.DateTimeField()


class Album(models.Model):
    name = models.CharField(max_length=64)
    year = models.DateTimeField()
    # folder = models.ImageField(upload_to'static/images')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)


