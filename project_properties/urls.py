from django.urls import path, include

from project_properties import views

urlpatterns = [
    path('direction_types_of_projects/', views.DirectionTypesListCreateAPIView.as_view()),
    path('direction_type_of_projects/<int:pk>/', views.DirectionTypeRetrieveUpdateDestroyAPIView.as_view()),
    path('types_of_projects/', views.ProjectTypesListCreateAPIView.as_view()),
    path('type_of_projects/<int:pk>/', views.ProjectTypeRetrieveUpdateDestroyAPIView.as_view()),

]
