from rest_framework import serializers

from project.models import Project, Task


class ProjectSerializer(serializers.ModelSerializer):
    order_title = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'
        extra_fields = ['order_title']


class ProjectSerializerWithoutDecription(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ('description', )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
