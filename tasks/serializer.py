from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Tag

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}, 'email': {'write_only' : True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ['url', 'title', 'description', 'status',
        'creation_date', 'finish_date', 'tags', 'owner']


class TagSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tag
        fields = ['url', 'title', 'date', 'tasks', 'owner']