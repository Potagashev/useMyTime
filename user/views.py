from rest_framework import generics

from user.models import User
from user.serializers import CustomUserSerializer


class EmployeesListAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return User.objects.filter(manager=self.request.user)
