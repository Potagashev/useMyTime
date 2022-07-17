from django.urls import path, include, re_path

from user import views

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    path('api/employees_of_current_user/', views.EmployeesListAPIView.as_view()),
]
