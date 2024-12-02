from rest_framework import serializers
from .models import User, Profile, Workout, WorkoutPlan, BlogPost, ProgressTracking

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'full_name', 'role']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'age', 'height', 'weight', 'fitness_level', 'goals', 'progress']

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'title', 'type', 'level', 'duration', 'video_url', 'description', 'instructions']

class WorkoutPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = ['id', 'user', 'workout', 'scheduled_date']

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']

class ProgressTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressTracking
        fields = ['id', 'user', 'date', 'weight', 'body_fat_percentage', 'muscle_mass', 'notes']

class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    workout_plans = WorkoutPlanSerializer(many=True, read_only=True)
    blog_posts = BlogPostSerializer(many=True, read_only=True)
    progress_tracking = ProgressTrackingSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'name',
            'role',
            'profile',
            'workout_plans',
            'blog_posts',
            'progress_tracking'
        ]
