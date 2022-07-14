from rest_framework import generics

from project.models import Project, Task
from project.serializers import ProjectSerializer, TaskSerializer


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(users__id=self.request.user.id)


class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


# список таск по проекту создание таски к проекту
class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(project=self.kwargs.get('project_id'))


# создание таски к проекту
class TaskCreateAPIView(generics.CreateAPIView):
    serializer_class = TaskSerializer


# почти что круд по айдишнику таски
class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


# список таск по юзеру
class TasksByUserListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    lookup_field = 'assignee__username'

    def get_queryset(self):
        return Task.objects.filter(
            assignee__username=self.kwargs.get('assignee__username')
        )
