from rest_framework import permissions

from rest_framework.permissions import SAFE_METHODS

from project.models import Project
from user.models import User


class IsProjectOwnerForTasks(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.project.owner.id == request.user.id


class IsHimself(permissions.BasePermission):
    def has_permission(self, request, view):
        return str(request.user.id) == view.kwargs.get('assignee__id')


class IsUsersManager(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.id, User.objects.get(id=view.kwargs.get('assignee__id')).manager.id)
        return request.user.id == User.objects.get(id=view.kwargs.get('assignee__id')).manager.id


class IsTaskAssignee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assignee.id == request.user.id


class IsProjectOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner.id == request.user.id


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsProjectMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in Project.objects.get(id=view.kwargs.get('id')).users.all()


class IsProjectMemberForTasks(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user in Project.objects.get(id=view.kwargs.get('project_id')).users.all()

    def has_object_permission(self, request, view, obj):
        return request.user in obj.project.users.all()