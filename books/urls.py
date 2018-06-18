from django.urls import path, include
from django.conf.urls import url
from dysk import settings
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout

urlpatterns = (
     path('', views.main),
     path('login/', views.login),
     path('registration/', views.registration),
     path('cloud_menu/', views.cloud_menu),
     path('storage_control/', views.storage_control),
     path('main/', views.main),
     path('about/', views.about),
     path('storage_control/directory_create/', views.directory_create),
     path('storage_control/file_upload', views.file_upload),
     path('paste/', views.paste),
     url('media/^', views.error_404_view),
     url('directory/(\d+)/$', views.change_directory),
     url('download/(\d+)/$', views.file_available),
     url('remove/(\d+)/$', views.remove),
     url('rename/(\d+)/$', views.rename),
     url('move/(\d+)/$', views.move),
     url('directoryRemove/(\d+)/$', views.directoryRemove),
     url('share/(\d+)/$', views.share_file),
     url('^', include('django.contrib.auth.urls')),
     url('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
)
