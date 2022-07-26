from rest_framework import serializers

from project_properties.models import DirectionType, ProjectType, Order


class DirectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectionType
        fields = '__all__'


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
