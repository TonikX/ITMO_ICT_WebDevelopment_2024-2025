from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ref_name = "FitnessUser"
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'is_superuser']

class ProgressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Progress
        fields = ['id', 'user', 'date', 'weight', 'notes']

class WorkoutPlanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = ['id', 'user', 'title', 'description', 'created_at']

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'title', 'description', 'video_url', 'level', 'workout_type', 'duration_minutes', 'created_at']

class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']

class WorkoutDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'title', 'description', 'video_url', 'level', 'workout_type', 'duration_minutes', 'created_at']
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.video_url = validated_data.get('video_url', instance.video_url)
        instance.level = validated_data.get('level', instance.level)
        instance.workout_type = validated_data.get('workout_type', instance.workout_type)
        instance.duration_minutes = validated_data.get('duration_minutes', instance.duration_minutes)
        instance.save()
        return instance
