import io
import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from project.models import Project, Task, Order
from project.permissions import ReadOnly, IsProjectMember, IsProjectOwner, IsProjectMemberForTasks, \
    IsProjectOwnerForTasks, IsTaskAssignee, IsUsersManager, IsHimself
from project.serializers import ProjectSerializer, TaskSerializer, ProjectSerializerWithoutDescription
from project.utils import validate_members, create_task
from project_properties.models import ProjectType, DirectionType


class ProjectListAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializerWithoutDescription

    def get_queryset(self):
        return Project.objects.filter(users__id=self.request.user.id)


class ProjectCreateViewSet(viewsets.ViewSet):
    @swagger_auto_schema(request_body=ProjectSerializer, operation_description='в order передаешь наименование заказа')
    def create(self, request):

        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        members = data['users']
        validated_members = validate_members(user_id=request.user.id, members=members)
        validated_members.append(request.user.id)

        data['users'] = validated_members

        serializer = ProjectSerializer(data=data)
        serializer.is_valid()
        serializer.save()

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
    @swagger_auto_schema(request_body=TaskSerializer)
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
