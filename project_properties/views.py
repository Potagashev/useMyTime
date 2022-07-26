from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from project_properties.models import DirectionType, ProjectType
from project_properties.serializers import DirectionTypeSerializer, ProjectTypeSerializer


class DirectionTypesListCreateAPIView(generics.ListCreateAPIView):
    """get all directions or add new direction type of project"""
    serializer_class = DirectionTypeSerializer
    queryset = DirectionType.objects.all()
    permission_classes = [IsAdminUser]


class DirectionTypeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """retrieve, update, or destroy direction type of project"""
    serializer_class = DirectionTypeSerializer
    queryset = DirectionType.objects.all()
    permission_classes = [IsAdminUser]


class ProjectTypesListCreateAPIView(generics.ListCreateAPIView):
    """get all projects types or add new type of project"""
    serializer_class = ProjectTypeSerializer
    permission_classes = [IsAdminUser]
    queryset = ProjectType.objects.all()


class ProjectTypeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """retrieve, update, or destroy type of project"""
    serializer_class = ProjectTypeSerializer
    queryset = ProjectType.objects.all()
    permission_classes = [IsAdminUser]
