from django.http import Http404
from rest_framework import permissions

from project.models import Task, Project
from timer.constants import PROJECT_NOT_FOUND_RESPONSE
from timer.models import TaskTimer


class IsAssigneeForTimer(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            task = Task.objects.get(id=view.kwargs['pk'])
        except Task.DoesNotExist:
            raise Http404
        return task.assignee == request.user


class IsProjectMemberForTimer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user in Project.objects.get(id=view.kwargs['pk']).users.all()


# class IsProjectMemberWithParams(permissions.BasePermission):
#     def has_permission(self, request, view):
#         project_id =
#         try:
#             project = Project.objects.get(id=request.query_params.get('project_id'))
#         except Project.DoesNotExist:
#             return PROJECT_NOT_FOUND_RESPONSE
#         return request.user.id in Project.objects.get
