from django.urls import path, include, re_path

from user import views

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    path('user/employees_of_current_user/', views.EmployeesListAPIView.as_view()),
    path('user/preview_users_by_ids/', views.EmployeesPreviewByIDsAPIView.as_view()),
    path('user/make_user_admin/<int:pk>/', views.MakeUserAdminAPIView.as_view()),
    path('email/send_email_to_developers/', views.SendEmailToDevelopersAPIView.as_view()),

    path('email/send_invite_to_email/', views.SendProjectInviteToEmailAPIView.as_view()),
    path('email/accept_the_invitation/', views.AcceptInvitationAPIView.as_view()),

]
