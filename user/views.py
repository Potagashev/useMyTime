from django.core.mail import send_mail
from django.http import Http404
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


class EmployeesPreviewByIDsAPIView(generics.ListAPIView):
    serializer_class = PreviewCustomUserSerializer

    def get_queryset(self):
        return User.objects.filter(id__in=self.request.data['users'])


class MakeUserAdminAPIView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]

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
            [developer_email],
            fail_silently=False,
        )
        if mail:
            return Response(status=200, data={'details': 'the email has been sent'})
        else:
            return Response(status=418, data={'details': 'something went wrong!'})