from posixpath import basename
from django.urls import path, include, re_path

import views

urlpatterns = [
    path('api/v1/users/', views.UserViewSet, basename='user'),
]