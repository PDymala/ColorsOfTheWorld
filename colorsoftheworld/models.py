from django.db import models
from django.db.models import CASCADE
from django.utils import timezone


class Website(models.Model):
    url = models.CharField(max_length=100)
    search = models.BooleanField(default=True)
    show = models.BooleanField(default=True)
    # search_results = models.ForeignKey(SearchResult, on_delete=CASCADE)

class SearchResult(models.Model):
    # url = models.CharField(max_length=100)
    url = models.ForeignKey(Website, on_delete=CASCADE, default=None)
    search_date = models.DateField(default=timezone.now())
    average_color = models.CharField(max_length=8)
    std_color = models.CharField(max_length=8)


class Cluster(models.Model):
    cluster_number = models.IntegerField(default=0)
    color = models.CharField(max_length=8)
    search_result_id = models.ForeignKey(SearchResult, on_delete=CASCADE)

class Quote(models.Model):
    quote_text = models.CharField(max_length=500)
    author = models.CharField(max_length=40)


#TODO KLASA Z PARAMETRAMI szukania ? tak aby nie grzebac w kodzie?