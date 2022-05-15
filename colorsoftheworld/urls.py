from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('starter', views.starter),
    path('image', views.image_from_database)
]