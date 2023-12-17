from rest_framework import serializers
from .models import Task,Subtask,UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields="__all__"

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields="__all__"

class TaskSerializer(serializers.ModelSerializer):
    subtasks=SubtaskSerializer(many=True,read_only=True)
    class Meta:
        model = Task
        fields=['id', 'title', 'percentage', 'subtasks','user']

