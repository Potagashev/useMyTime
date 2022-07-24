from django.urls import path, re_path

from project import views

urlpatterns = [
    path('projects_of_current_user/', views.ProjectListAPIView.as_view()),
    path('create_project/', views.ProjectCreateViewSet.as_view({'post': 'create'})),
    path('add_task_to_project/', views.TaskCreateAPIView.as_view()),
    re_path('^(?P<id>.+)/$', views.ProjectRetrieveUpdateDestroyAPIView.as_view()),

    re_path('^tasks_of_project/(?P<project_id>.+)/$', views.TaskListAPIView.as_view()),
    path('add_task_to_project/', views.TaskCreateAPIView.as_view()),
    re_path('^task/(?P<id>.+)/$', views.TaskRetrieveUpdateDestroyAPIView.as_view()),
    re_path('^tasks_by_assignee/(?P<assignee__id>.+)/$', views.TasksByUserListAPIView.as_view()),
]
