from django.urls import path

from report import views

urlpatterns = [
    path('get_report_for_period/', views.GetReportForPeriod.as_view())
]