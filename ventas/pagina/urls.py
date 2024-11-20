from django.contrib import admin
from django.urls import path
from .views import index,about,client,log_in,register,adminpage,adminusuarios,inventarioadmin,vendedor, signup, signin, logout_view

urlpatterns = [
    path('',index,name="index"),
    path('logout/', logout_view, name='logout'),  
    path('about/',about,name="about"),
    path('client/',client,name="client"),
    path('log_in/',log_in,name="log_in"),
    path('register/',register,name="register"),
    path('adminpage/',adminpage,name="adminpage"),
    path('adminusuarios/',adminusuarios,name="adminusuarios"),
    path('inventarioadmin/',inventarioadmin,name="inventarioadmin"),
    path('vendedor/',vendedor,name="vendedor"),
    path('signup/', signup, name="signup"),
    path('signin/', signin, name="signin"),
    
]