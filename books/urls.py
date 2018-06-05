from django.urls import path, include
from django.conf.urls import url

from dysk import settings
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout

urlpatterns = (
     path('', views.index),
     path('login/', views.login),
     path('registration/', views.registration),
     path('cloud_menu/', views.cloud_menu),
     path('storage_control/', views.storage_control),
     path('main/', views.main),
     path('about/', views.about),
     path('storage_control/', views.storage_control),
     url('^', include('django.contrib.auth.urls')),
     url('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout')
)
