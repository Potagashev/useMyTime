from rest_framework import permissions


class IsProgramTimerOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            task = Task.objects.get(id=view.kwargs['pk'])
        except Task.DoesNotExist:
            raise Http404
        return task.assignee == request.user


class IsProjectMemberForTimer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user in Project.objects.get(id=view.kwargs['pk']).users.all()
