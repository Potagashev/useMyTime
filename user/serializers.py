from rest_framework import serializers

from user.models import User


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'is_staff',
            'username',
            'first_name',
            'last_name',
            'email',
            'department',
            'appointment',
            'manager',
        ]


class PreviewCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'displayName']


class CustomUserStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'displayName', 'is_staff']
