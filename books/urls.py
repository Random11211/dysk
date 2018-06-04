from django.urls import path
from . import views

urlpatterns = (
     path('', views.index),
     path('login/', views.login),
     path('registration/', views.registration),
     path('cloud_menu/', views.cloud_menu),
     path('storage_control/', views.storage_control),
     path('main/', views.main),
     path('about/', views.about)
)
