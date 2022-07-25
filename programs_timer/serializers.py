from rest_framework import serializers

from programs_timer.models import ProgramTimer, Program


class ProgramTimerSerializerForStarting(serializers.ModelSerializer):
    class Meta:
        model = ProgramTimer
        exclude = ('end_time', )


class ProgramTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramTimer
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'
