from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from project.models import Project
from project.permissions import IsProjectMember
from project.serializers import ProjectSerializer, ProjectSerializerWithoutDescription


class FilterProjectsAPIView(generics.ListAPIView):
    """filtering can be priority, name, start_time, end_time, order, type, direction_type"""
    serializer_class = ProjectSerializerWithoutDescription
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """there can be priority, name, start_time, end_time, order, type, direction_type"""
        param = self.request.query_params.get('filter_by')
        if param:
            return Project.objects.filter(users__id=self.request.user.id).order_by(param)
        else:
            return Project.objects.filter(users__id=self.request.user.id)
