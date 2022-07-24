from rest_framework import serializers

from timer.models import TaskTimer


class TaskTimerSerializerForStarting(serializers.ModelSerializer):
    class Meta:
        model = TaskTimer
        exclude = ('end_time', )


class TaskTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTimer
        fields = '__all__'
