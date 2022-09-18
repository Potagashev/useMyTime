from django.urls import path, re_path

from timer import views

urlpatterns = [
    path('start_task_timer/', views.StartTaskTimerAPIView.as_view()),
    path('stop_task_timer/', views.StopTaskTimerAPIView.as_view()),

    path('timer_info_by_task/', views.TimerInfoByTaskAPIView.as_view()),
    path('timer_info_by_project_for_today/<int:pk>/', views.TimerInfoByProjectForTodayAPIView.as_view()),
    path('total_time_by_project/<int:pk>/', views.TotalTimeByProjectAPIView.as_view()),
    path('total_time_by_task/<int:pk>/', views.TotalTimeByTaskAPIView.as_view()),

    path('sessions_by_project/<int:pk>/', views.SessionsByProjectAPIView.as_view()),
    path('sessions_by_task/<int:pk>/', views.SessionsByTaskAPIView.as_view()),
    path('sessions_by_project_for_period/<int:pk>', views.SessionsByProjectForThePeriodAPIView.as_view()),
    path('sessions_by_task_for_period/<int:pk>', views.SessionsByTaskForPeriodAPIView.as_view()),

    path('project_statistics_for_last_two_weeks/<int:pk>', views.ProjectStatisticsForLastTwoWeeks.as_view())
]
