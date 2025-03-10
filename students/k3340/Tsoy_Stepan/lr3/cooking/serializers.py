from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from cooking.models import Meal, Step, Comment, Like


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class MealListSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    difficulty = serializers.SerializerMethodField()

    class Meta:
        model = Meal
        fields = [
            'id',
            'author',
            'title',
            'headline',
            'banner',
            'difficulty'
        ]

    def get_difficulty(self, obj):
        return obj.get_difficulty_display()


class MealDetailSerializer(ModelSerializer):
    difficulty = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Meal
        fields = '__all__'

    def get_difficulty(self, obj):
        return obj.get_difficulty_display()


class MealCreateSerializer(ModelSerializer):
    difficulty = serializers.ChoiceField(choices=Meal.DIFFICULTY_CHOICES)

    class Meta:
        model = Meal
        fields = [
            'title',
            'headline',
            'banner',
            'ingredients',
            'video',
            'difficulty'
        ]


class StepSerializer(ModelSerializer):
    class Meta:
        model = Step
        fields = [
            'step_number',
            'step_description',
            'attachment'
        ]
        read_only_fields = ['step_number']


class CommentSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['author', 'text', 'rating', 'dt_published']
        read_only_fields = ['dt_published']


class LikeSerializer(ModelSerializer):
    meal = MealListSerializer()

    class Meta:
        model = Like
        fields = ['meal', 'status']
