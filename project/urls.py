from django.urls import path, re_path

from project import views

urlpatterns = [
    path('api/projects_of_current_user/', views.ProjectListAPIView.as_view()),
    path('api/create_project/', views.ProjectCreateViewSet.as_view({'post': 'create'})),
    re_path('^api/project/(?P<id>.+)/$', views.ProjectRetrieveUpdateDestroyAPIView.as_view()),

    re_path('^api/tasks_of_project/(?P<project_id>.+)/$', views.TaskListAPIView.as_view()),
    path('api/add_task_to_project/', views.TaskCreateAPIView.as_view()),
    re_path('^api/task/(?P<id>.+)/$', views.TaskRetrieveUpdateDestroyAPIView.as_view()),
    re_path('^api/tasks_by_assignee/(?P<assignee__id>.+)/$', views.TasksByUserListAPIView.as_view()),
]
