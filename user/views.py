import json

from django.core.mail import send_mail
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user import constants
from user.models import User
from user.serializers import PreviewCustomUserSerializer, CustomUserStaffSerializer


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
        subject = constants.SUBJECT
        message_header = f"От кого: {self.request.user.displayName}\n" \
                         f"Почта: {self.request.user.email}\n\n"
        message = message_header + self.request.data['message']
        developer_email = constants.DEVELOPER_EMAIL
        mail = send_mail(
            subject,
            message,
            'alexpotagashev@gmail.com',
            [developer_email, 'dapasynkov2001@gmail.com'],
            fail_silently=False,
        )
        if mail:
            return Response(status=200, data={'details': 'the email has been sent'})
        else:
            return Response(status=418, data={'details': 'something went wrong!'})
