from rest_framework import serializers

from project.models import Project, Task


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        try:
            users = validated_data.pop('users')
        except KeyError:
            users = []
        project = Project.objects.create(**validated_data)
        project.users.set([user.id for user in users])
        project.save()
        return project


class ProjectSerializerWithoutDescription(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ('description', )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
