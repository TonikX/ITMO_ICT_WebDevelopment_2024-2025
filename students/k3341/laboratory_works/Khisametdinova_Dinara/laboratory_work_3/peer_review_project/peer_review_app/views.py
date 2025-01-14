from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from django.db.models import Avg, IntegerField
from django.db.models.functions import Cast
from .models import User, Task, Criterion, Option, Submission, Review
from .serializers import (
    UserSerializer, TaskSerializer, CriterionSerializer,
    OptionSerializer, SubmissionSerializer, ReviewSerializer, TaskDetailSerializer
)

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsTeacher]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

class TaskDetailWithRelationsView(RetrieveUpdateAPIView):
    """
    API View для получения и редактирования задачи с вложенными критериями и опциями.
    """
    queryset = Task.objects.prefetch_related('criterion_set', 'option_set').all()
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.creator:
            raise PermissionDenied("Только создатель задачи может ее редактировать.")
        serializer.save()

class CriterionListCreateView(generics.ListCreateAPIView):
    queryset = Criterion.objects.all()
    serializer_class = CriterionSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

class CriterionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Criterion.objects.all()
    serializer_class = CriterionSerializer
    permission_classes = [IsAuthenticated]

class OptionListCreateView(generics.ListCreateAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

class OptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated]

class SubmissionListCreateView(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['task', 'user']
    search_fields = ['content']
    ordering_fields = ['submitted_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class TaskStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        task_count = Task.objects.count()
        submission_count = Submission.objects.count()
        review_count = Review.objects.count()
        return Response({
            "tasks": task_count,
            "submissions": submission_count,
            "reviews": review_count
        })
    
class AverageScoreView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
            avg_score = Review.objects.filter(submission__task=task).annotate(
                score_as_int=Cast('score', IntegerField())
            ).aggregate(Avg('score_as_int'))['score_as_int__avg']
            return Response({
                "task": task.title,
                "average_score": avg_score if avg_score is not None else "No reviews yet"
            })
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)
