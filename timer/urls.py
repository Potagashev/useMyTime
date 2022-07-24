from django.urls import path, re_path

from timer import views

urlpatterns = [
    path('start_task_timer/<int:pk>/', views.StartTaskTimerAPIView.as_view()),
    path('stop_task_timer/', views.StopTaskTimerAPIView.as_view()),

    path('timer_info_by_task/', views.TimerInfoByTaskAPIView.as_view()),
    path('timer_info_by_project_for_today/<int:pk>/', views.TimerInfoByProjectForTodayAPIView.as_view())
]
