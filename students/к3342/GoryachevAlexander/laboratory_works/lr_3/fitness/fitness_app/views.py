from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from datetime import datetime



from .models import (
    BlogPost,
    Workout,
    UserWorkout,
    User,
)

from .serializers import (
    CustomUserSerializer,
    BlogPostSerializer,
    UserWorkoutGetSerializer,
    WorkoutSerializer,
    UserWorkoutSerializer,
    BlogPostSerializerByDateAuthors,
)

class BlogViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """список всех постов"""
        blogs = BlogPost.objects.all()
        category = request.query_params.get('category')
        author_id = request.query_params.get('author_id')

        if category:
            blogs = blogs.filter(category=category)
        if author_id:
            blogs = blogs.filter(author_id=author_id)

        serializer = BlogPostSerializer(blogs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """просмотр поста"""
        blog = get_object_or_404(BlogPost, id=pk)
        serializer = BlogPostSerializer(blog)
        return Response(serializer.data)

    def create(self, request):
        """создание нового поста"""
        serializer = BlogPostSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'delete'])
    def manage(self, request, pk=None):
        """обновить или удалить пост"""
        blog = get_object_or_404(BlogPost, id=pk)

        # Проверка на авторство
        if blog.author != request.user:
            return Response(
                {"error": "Not authorized to modify this post"},
                status=status.HTTP_403_FORBIDDEN
            )

        if request.method == 'DELETE':
            blog.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = BlogPostSerializer(
            blog,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Get all authors by date.",
        responses={200: BlogPostSerializerByDateAuthors},
        manual_parameters=[
            openapi.Parameter(
                'date', openapi.IN_QUERY,
                description="Date.",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    @action(detail=False, methods=['get'], url_path='authors_by_date')
    def authors_by_date(self, request):
        """Показывает всех авторов, чьи статьи были опубликованы в указанную дату"""
        date_param = request.query_params.get('date')

        if not date_param:
            return Response({"error": "Параметр 'date' обязателен."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            date = datetime.strptime(date_param, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Неверный формат даты. Используйте формат YYYY-MM-DD."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Фильтруем статьи, опубликованные в указанную дату
        blogs = BlogPost.objects.filter(created_at__date=date)

        # Вытаскиваем авторов, чьи статьи были опубликованы в эту дату
        authors = set(blogs.values_list('author', flat=True))

        # Загружаем данные пользователей (авторов), при этом добавляем информацию о статьях каждого автора
        author_data = User.objects.filter(id__in=authors)

        # Сериализуем авторов и их посты
        serializer = BlogPostSerializerByDateAuthors(author_data, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """список всех тренировок"""
        workouts = Workout.objects.all()
        workout_type = request.query_params.get('type')

        if workout_type:
            workouts = workouts.filter(type=workout_type)

        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """подробности тренировки"""
        workout = get_object_or_404(Workout, id=pk)
        serializer = WorkoutSerializer(workout)
        return Response(serializer.data)

    def create(self, request):
        """создать новую тренировку"""
        serializer = WorkoutSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """начать тренировку"""
        workout = get_object_or_404(Workout, id=pk)
        user_workout = UserWorkout.objects.create(
            user=request.user,
            workout=workout,
            started_at=timezone.now()
        )
        serializer = UserWorkoutSerializer(user_workout)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """закончить тренировку"""
        user_workout = get_object_or_404(
            UserWorkout,
            id=pk,
            user=request.user,
            completed_at__isnull=True
        )
        user_workout.completed_at = timezone.now()
        user_workout.save()
        serializer = UserWorkoutSerializer(user_workout)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def history(self, request):
        """история тренировок пользователя"""
        user_workouts = UserWorkout.objects.filter(user=request.user)
        serializer = UserWorkoutGetSerializer(user_workouts, many=True)
        return Response(serializer.data)

class AccountViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """информация о пользователе"""
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

    def update(self, request):
        """обновить информацию о пользователе"""
        user = request.user
        serializer = CustomUserSerializer(
            user,
            data=request.data,
            context={'request': request},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)