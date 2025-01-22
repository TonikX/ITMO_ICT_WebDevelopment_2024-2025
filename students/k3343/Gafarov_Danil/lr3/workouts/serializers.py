from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import *


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class StepSerializer(serializers.Serializer):
    step = serializers.CharField()

    def to_representation(self, value):
        return value.step_description


class TagSerializer(serializers.Serializer):
    tag = serializers.CharField()

    def to_representation(self, value):
        return value.tag_name


class WorkoutDetailSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=255), write_only=True
    )
    tags_display = serializers.SerializerMethodField()
    steps = serializers.ListField(
        child=serializers.CharField(max_length=255), write_only=True
    )
    steps_display = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField(read_only=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Workout
        fields = '__all__'

    def get_tags_display(self, obj):
        return [tag.tag_name for tag in obj.tags.all()]

    def get_steps_display(self, obj):
        return [step.step_description for step in obj.steps.all()]

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        step_data = validated_data.pop('steps', [])
        workout = super().create(validated_data)
        self._handle_tags(workout, tags_data)
        self._handle_steps(workout, step_data)
        return workout

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        step_data = validated_data.pop('steps', [])
        workout = super().update(instance, validated_data)
        self._handle_tags(workout, tags_data)
        self._handle_steps(workout, step_data)
        return workout

    def _handle_tags(self, workout, tags_data):
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(tag_name=tag_name)
            tags.append(tag)
        if tags:
            workout.tags.set(tags)

    def _handle_steps(self, workout, steps_data):
        steps = []
        for step_description in steps_data:
            step, created = Step.objects.get_or_create(step_description=step_description)
            steps.append(step)
        if steps:
            workout.steps.set(steps)

    def get_rating(self, obj):
        return obj.comment_set.aggregate(models.Avg('rating'))['rating__avg']


class WorkoutListSerializer(ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'author', 'title', 'time_takes', 'rating']

    def get_rating(self, obj):
        return obj.comment_set.aggregate(models.Avg('rating'))['rating__avg']


class CommentListSerializer(ModelSerializer):
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'title', 'comment', 'dt_published', 'rating']



class RoutineListSerializer(ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Routine
        fields = ['id', 'author', 'title', 'tags']

    def get_tags(self, obj):
        return [tag.tag_name for tag in obj.tags.all()]

class RoutineSerializer(ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=255), write_only=True
    )
    tags_display = serializers.SerializerMethodField()
    workouts = WorkoutListSerializer(many=True, read_only=True)

    class Meta:
        model = Routine
        fields = '__all__'

    def get_tags_display(self, obj):
        return [tag.tag_name for tag in obj.tags.all()]

    def _handle_tags(self, workout, tags_data):
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(tag_name=tag_name)
            tags.append(tag)
        workout.tags.set(tags)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        routine = Routine.objects.create(**validated_data)
        self._handle_tags(routine, tags_data)
        return routine

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        routine = super().update(instance, validated_data)
        self._handle_tags(routine, tags_data)
        return routine
