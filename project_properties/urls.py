from django.urls import path, include

from project_properties import views

urlpatterns = [
    path('api/direction_types_of_projects', views.DirectionTypesListCreateAPIView.as_view()),
    path('api/direction_type_of_projects/<int:pk>', views.DirectionTypeRetrieveUpdateDestroyAPIView.as_view()),
    path('api/types_of_projects', views.ProjectTypesListCreateAPIView.as_view()),
    path('api/type_of_project', views.ProjectTypeRetrieveUpdateDestroyAPIView.as_view()),
]
