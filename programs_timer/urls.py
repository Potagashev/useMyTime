from django.urls import path, include

from programs_timer import views

urlpatterns = [
    path('start_program_timer/', views.StartProgramTimerAPIView.as_view()),
    path('stop_program_timer/', views.StopProgramTimerAPIView.as_view()),

    path('program_timer_info_by_program/<int:pk>/', views.ProgramTimerInfoByProgramAPIView.as_view()),
    path('programs/', views.ProgramsListAPIView.as_view()),

    path('program_timer_info_by_program_for_period/', views.ProgramTimerInfoByProgramForPeriodAPIView.as_view()),
]
