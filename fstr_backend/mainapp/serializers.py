from rest_framework import serializers

from .models import User, Area, MountainPass


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class MountainPassSerializer(serializers.ModelSerializer):

    class Meta:
        model = MountainPass
        fields = '__all__'
