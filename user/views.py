import json

from django.core.mail import send_mail
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.models import Membership, Project
from user import constants
from user.constants import INVITATION_HAS_ALREADY_ACCEPTED_RESPONSE, MEMBERSHIP_NOT_FOUND, INVITATION_ACCEPTED_RESPONSE
from user.models import User
from user.serializers import PreviewCustomUserSerializer, CustomUserStaffSerializer
from user.utils import send_invites, send_email_to_developers


class EmployeesListAPIView(generics.ListAPIView):
    serializer_class = PreviewCustomUserSerializer

    def get_queryset(self):
        return User.objects.filter(manager=self.request.user)


class EmployeesPreviewByIDsAPIView(APIView):
    """<h2>Request: {"users": [1, 2, 3, 4,.....]}</h2>"""
    serializer_class = PreviewCustomUserSerializer

    @swagger_auto_schema(
        operation_description='<h2>Request: {"users": [1, 2, 3, 4,.....]}\n'
                              'Responses: 200 - [ {"id": 3, "displayName": null }, ...]</h2>'
    )
    def post(self, request):
        users = User.objects.filter(id__in=self.request.data['users'])
        serializer = PreviewCustomUserSerializer(users, many=True)
        return Response(serializer.data)


class MakeUserAdminAPIView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

    @swagger_auto_schema(operation_description='<h2>this request needs only ID\n'
                                               'Response: 200 - id, displayName, is_staff</h2>')
    def patch(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404
        user.is_staff = True
        user.save()
        serializer = CustomUserStaffSerializer(user)
        return Response(status=200, data=serializer.data)


class SendEmailToDevelopersAPIView(APIView):
    @swagger_auto_schema(operation_description='<h2>Request: {"message": "{your_message}"}\n'
                                               'Response: \n200 - {"details": "the email has been sent"}\n'
                                               '418 - {"details": "something went wrong!"}</h2>')
    def post(self, request):
        message_header = f"От кого: {self.request.user.displayName}\n" \
                         f"Почта: {self.request.user.email}\n\n"
        message = message_header + self.request.data['message']
        send_email_to_developers(message=message)


class SendProjectInviteToEmailAPIView(APIView):
    @swagger_auto_schema(operation_description='<h2>Request: {"project_id": 123, "users": [1, 2, 3]}\n'
                                               'Response: \n200 - {"details": "the email has been sent"}\n'
                                               '418 - {"details": "something went wrong!"}</h2>')
    def post(self, request):
        project_id = self.request.data['project_id']
        users = self.request.data['users']
        emails = []
        for user_id in users:
            user = User.objects.get(id=user_id)
            membership = Membership()
            membership.project = Project.objects.get(id=project_id)
            membership.user = user
            membership.is_confirmed = False
            membership.save()

            emails.append(user.email)
        send_invites(emails)


class AcceptInvitationAPIView(APIView):
    @swagger_auto_schema(operation_description='<h2>Request: {"project_id": 123, "user_id": 345}\n'
                                               'Response: \n200 - {"details": "invitation accepted"}'
                                               '\n404 - {"details": "this user was not invited in this project"}'
                                               '\n403 - {"details": "invintation has already accepted"}</h2>')
    def post(self, request):
        project_id = self.request.data['project_id']
        user_id = self.request.data['user_id']
        try:
            membership = Membership.objects.get(user__id=user_id, project__id=project_id)
        except Membership.DoesNotExist:
            return MEMBERSHIP_NOT_FOUND
        if membership.is_confirmed:
            return INVITATION_HAS_ALREADY_ACCEPTED_RESPONSE

        membership.is_confirmed = True
        membership.save()
        return INVITATION_ACCEPTED_RESPONSE
