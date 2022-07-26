from rest_framework import serializers

from project_properties.models import DirectionType, ProjectType


class DirectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectionType
        fields = '__all__'


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = '__all__'
