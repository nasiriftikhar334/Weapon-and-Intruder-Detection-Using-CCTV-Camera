"""weapon_detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from .views import index
from detection.alert import alertstream
from detection.views import (
    video_feed,
    camera_list_view,
    camera_add_view,
    camera_detail_view
)
from account.views import (
    login_view,
    logout_view
)

urlpatterns = [
    path('', index, name='index'),
    path('video_feed<int:cam>', video_feed, name='video_feed'),
    path('stream/', alertstream, name='alertstream'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cameras/', camera_list_view, name='camera-list'),
    path('cameras/add/', camera_add_view, name='camera-add'),
    path('cameras/<str:name>/', camera_detail_view, name='camera-detail'),
]
