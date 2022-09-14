import json

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from project.models import Project, Task
from project.permissions import ReadOnly, IsProjectMember, IsProjectOwner, IsProjectMemberForTasks, \
    IsProjectOwnerForTasks, IsTaskAssignee, IsUsersManager, IsHimself
from project.serializers import ProjectSerializer, TaskSerializer, ProjectSerializerWithoutDescription
from project.utils import create_task, validate_data_for_project_creating


class ProjectPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 10000


class ProjectListAPIView(generics.ListAPIView):
    """
    <h3>filtering can be priority, name, start_time, end_time, order, type, direction_type
    REQUIRED REQUEST FORMAT: project/projects_of_current_user/?filter_by={field}</h3>
    """
    serializer_class = ProjectSerializerWithoutDescription
    pagination_class = ProjectPagination

    def get_queryset(self):
        param = self.request.query_params.get('filter_by')
        if param:
            return Project.objects.filter(users__id=self.request.user.id).order_by(param)
        else:
            return Project.objects.filter(users__id=self.request.user.id).order_by('id')


class ProjectCreateViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=ProjectSerializer,
        operation_description="<h2>You don't have to provide OWNER</h2>"
                              "<h2>In ORDER field you should provide string as <u>name</u> of order</h2>"
    )
    def create(self, request):
        data = validate_data_for_project_creating(request)
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
    # """
    # <h2>filtering can be priority, name, description, project, assignee, deadline, fulfilled
    # REQUIRED REQUEST FORMAT: task/tasks_of_project/{project_id}/?filter_by={field}</h2>
    # """
    permission_classes = [IsProjectMemberForTasks]
    serializer_class = TaskSerializer
    lookup_field = 'project_id'

    def get_queryset(self):
        # param = self.request.query_params.get('filter_by')
        # if param:
        #     return Task.objects.filter(project=self.kwargs.get('project_id')).order_by(param)
        # else:
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
        project = Project.objects.get(id=data['project_id'])
        if request.user not in project.users.all():
            return Response(data={"detail": "You do not have permission to perform this action."}, status=403)

        task = create_task(request)
        print(task)
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
