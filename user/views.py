from rest_framework import generics

from user.models import User
from user.serializers import CustomUserSerializer, PreviewCustomUserSerializer


class EmployeesListAPIView(generics.ListAPIView):
    serializer_class = PreviewCustomUserSerializer

    def get_queryset(self):
        return User.objects.filter(manager=self.request.user)


class EmployeesPreviewByIDsAPIView(generics.ListAPIView):
    serializer_class = PreviewCustomUserSerializer

    def get_queryset(self):
        return User.objects.filter(id__in=self.request.data['users'])
