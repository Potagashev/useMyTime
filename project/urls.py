from django.urls import path, include, re_path

from project import views

urlpatterns = [
    path('api/projects', views.ProjectListCreateAPIView.as_view()),
    path('api/project/<int:pk>', views.ProjectRetrieveUpdateDestroyAPIView.as_view()),

    path('api/tasks_of_project/<int:project_id>', views.TaskListAPIView.as_view()),
    path('api/add_task_to_project', views.TaskCreateAPIView.as_view()),
    path('api/task/<int:pk>', views.TaskRetrieveUpdateDestroyAPIView.as_view()),
    re_path('^api/tasks_by_assignee/(?P<assignee__username>.+)/$', views.TasksByUserListAPIView.as_view()),
]
