from django.urls import path
from . import views

urlpatterns = (
     path('', views.index),
     path('login/', views.login),
     path('registration/', views.registration),
     path('cloud_menu/', views.cloud_menu),
)
