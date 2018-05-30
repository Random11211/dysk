from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = (
     path('', views.index),
     path('login/', views.login),
     path('registration/', views.registration),
     path('cloud_menu/', views.cloud_menu),
     path('storage_control/', views.storage_control),
     url('^', include('django.contrib.auth.urls'))
)
