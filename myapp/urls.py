from os import abort
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
   path("",views.index,name="myapp"),
   path("about",views.about,name="about"),
   path("detector",views.detector,name="detector"),
    path("contactus",views.contactus,name="contactus"),
]
