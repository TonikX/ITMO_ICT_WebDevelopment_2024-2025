from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Workout, BlogPost, UserWorkout
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

User = get_user_model()


class CustomUserCreateSerializer(BaseUserCreateSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    re_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 're_password', 'email', 'level')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'level')
        read_only_fields = ('id',)


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class BlogPostTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для только названия статьи"""
    title = serializers.CharField()

    class Meta:
        model = BlogPost
        fields = ['title']  # Показываем только название статьи

class BlogPostSerializerByDateAuthors(serializers.ModelSerializer):
    """Сериализатор для авторов с только названиями статей"""
    name = serializers.CharField(source='username')  # Имя пользователя (автора)
    blog_posts = BlogPostTitleSerializer(many=True)  # Используем сериализатор с только названиями

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'blog_posts']


class UserWorkoutGetSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    workout = WorkoutSerializer(read_only=True)

    class Meta:
        model = UserWorkout
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UserWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkout
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
