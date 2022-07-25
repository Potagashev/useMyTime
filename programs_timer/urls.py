from django.urls import path, include

from programs_timer import views

urlpatterns = [
    path('start_program_timer/<int:pk>/', views.StartProgramTimerAPIView.as_view()),
    path('stop_program_timer/<int:pk>/', views.StopProgramTimerAPIView.as_view()),

    path('program_timer_info_by_program/<int:pk>/', views.ProgramTimerInfoByProgramAPIView.as_view()),
    path('programs/', views.ProgramsListAPIView.as_view()),

    path('program_timer_info_by_program_for_today/<int:pk>/', views.ProgramTimerInfoByProgramForTodayAPIView.as_view()),
]
