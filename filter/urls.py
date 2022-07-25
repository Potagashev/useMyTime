from django.urls import path

from filter import views

urlpatterns = [
    path('filter_projects/', views.FilterProjectsAPIView.as_view()),
]