import json

from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from project.models import Project, Task
from project.permissions import ReadOnly, IsProjectMember, IsProjectOwner, IsProjectMemberForTasks, \
    IsProjectOwnerForTasks, IsTaskAssignee, IsUsersManager, IsHimself
from project.serializers import ProjectSerializer, TaskSerializer, ProjectSerializerWithoutDecription
from project.utils import validate_members, create_task


class ProjectListAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializerWithoutDecription

    def get_queryset(self):
        return Project.objects.filter(users__id=self.request.user.id)


class ProjectCreateViewSet(viewsets.ViewSet):
    def create(self, request):
        data = json.loads(request.body)
        members = data['users']
        validated_members = validate_members(user_id=request.user.id, members=members)
        validated_members.append(request.user.id)

        project = Project.objects.create(
            name=data['name'],
            owner=request.user,
            description=data['description'],
            deadline=data['deadline'],
            priority=data['priority'],
        )
        project.users.set(validated_members)
        project.save()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)


class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectOwner | (ReadOnly & IsProjectMember)]
    lookup_field = 'id'

    def get_queryset(self):
        return Project.objects.filter(id=self.kwargs.get('id'))


# список таск по проекту
class TaskListAPIView(generics.ListAPIView):
    permission_classes = [IsProjectMemberForTasks]
    serializer_class = TaskSerializer
    lookup_field = 'project_id'

    def get_queryset(self):
        return Task.objects.filter(project=self.kwargs.get('project_id'))


# создание таски к проекту
class TaskCreateAPIView(APIView):
    # todo
    # отрефакторить, дописать permission classes
    def post(self, request):
        """получаем данные с запроса, проверяем участие юзера в проекте,
        если нет - 403
        далее проверяем принадлежность проекта юзеру,
        если да - он назначает юзера к задаче,
        иначе - задача назначается ему самому"""

        data = json.loads(request.body)
        project = Project.objects.get(id=data['project'])
        if request.user not in project.users.all():
            return Response(data={"detail": "You do not have permission to perform this action."}, status=403)

        task = create_task(request)
        serializer = TaskSerializer(task)
        return Response(serializer.data)


# почти что круд по айдишнику таски
class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsProjectOwnerForTasks | IsTaskAssignee | (ReadOnly & IsProjectMemberForTasks)]

    lookup_field = 'id'

    def get_queryset(self):
        return Task.objects.filter(id=self.kwargs.get('id'))


# список таск по юзеру
class TasksByUserListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    lookup_field = 'assignee__id'
    permission_classes = [IsHimself | IsUsersManager]

    def get_queryset(self):
        return Task.objects.filter(
            assignee__id=self.kwargs.get('assignee__id')
        )
