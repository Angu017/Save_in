
from django.contrib import admin
from django.urls import path
from .views import index,about,client,log_in,register

urlpatterns = [
    path('',index,name="index"),
    path('about/',about,name="about"),
    path('client/',client,name="client"),
    path('log_in/',log_in,name="log_in"),
    path('register/',register,name="register")
]
