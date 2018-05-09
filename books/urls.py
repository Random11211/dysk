from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = (
    path('', views.index),
    path('test/', views.test),
    path('test2/', views.test2),

)

