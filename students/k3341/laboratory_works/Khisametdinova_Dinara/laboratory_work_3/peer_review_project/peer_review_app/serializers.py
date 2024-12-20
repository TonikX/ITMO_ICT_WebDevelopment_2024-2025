from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ref_name = "PeerReviewUser"
        fields = ['id', 'email', 'role', 'username', 'first_name', 'last_name']

class TaskSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'creator']

class CriterionSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = Criterion
        fields = ['id', 'name', 'description', 'task']

class OptionSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = Option
        fields = ['id', 'content', 'task']

class SubmissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = Submission
        fields = ['id', 'user', 'task', 'content', 'submitted_at']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    submission = serializers.PrimaryKeyRelatedField(queryset=Submission.objects.all())
    criterion = serializers.PrimaryKeyRelatedField(queryset=Criterion.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'submission', 'user', 'criterion', 'comments', 'score']

'''
GET-запрос, возвращающий Submission c вложенными Review с китериями и опциями для связи Many-To-Many
'''
class TaskDetailSerializer(serializers.ModelSerializer):
    criterion = CriterionSerializer(many=True, read_only=True)
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'creator', 'criterion', 'options']
