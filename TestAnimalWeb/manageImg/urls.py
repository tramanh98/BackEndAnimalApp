from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from .views import *

app_name = 'manageImg'

urlpatterns = [
    path('api/img/upload/', PhotoUploadView.as_view()), # Upload photo
    path('api/img/delete/<pk>/', PhotoDelete.as_view()), # Xóa ảnh của bài đăng
]