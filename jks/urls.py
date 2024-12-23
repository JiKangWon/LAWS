"""
URL configuration for jks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main_site import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.get_home, name='home'),
    path('todo/id=<int:id>/', views.get_todolist, name='todolist'),
    path('todo/open/id=<int:id>/', views.get_open_shift, name='open_shift'),
    path('todo/close/id=<int:id>/', views.get_close_shift, name='close_shift'),
    path('todo/get-subject/',views.get_subject, name='get_subject'),
    path('todo/get-course/',views.get_course, name='get_course'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
