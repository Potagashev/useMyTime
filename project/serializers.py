from rest_framework import serializers

from project.models import Project, Task


class ProjectSerializer(serializers.ModelSerializer):
    order_title = serializers.CharField(max_length=30)

    class Meta:
        model = Project
        fields = (
            'name',
            'owner',
            'users',
            'description',
            'start_date',
            'end_date',
            'order_title',
            'type',
            'direction_type',
            'priority',
        )


class ProjectSerializerWithoutDescription(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ('description', )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
