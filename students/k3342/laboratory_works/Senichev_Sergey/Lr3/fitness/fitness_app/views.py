from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import (
    BlogPost,
    Workout,
    Trainer,
    UserWorkout,
)

from .serializers import (
    CustomUserSerializer,
    BlogPostSerializer,
    TrainerSerializer,
    WorkoutSerializer,
    UserWorkoutSerializer,
)


# Account related views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account_info(request):
    """информация о пользователе"""
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data)


# Workout related views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def workout_list(request):
    """список всех тренировок"""
    workouts = Workout.objects.all()
    trainer_id = request.query_params.get('trainer_id')
    workout_type = request.query_params.get('type')

    if trainer_id:
        workouts = workouts.filter(trainer_id=trainer_id)
    if workout_type:
        workouts = workouts.filter(type=workout_type)

    serializer = WorkoutSerializer(workouts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def workout_detail(request, id):
    """подробности тренировки"""
    workout = get_object_or_404(Workout, id=id)
    serializer = WorkoutSerializer(workout)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_workout(request):
    """создать новую тренировку"""
    serializer = WorkoutSerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_workout(request, workout_id):
    """начать тренировку"""
    workout = get_object_or_404(Workout, id=workout_id)
    user_workout = UserWorkout.objects.create(
        user=request.user,
        workout=workout,
        started_at=timezone.now()
    )
    serializer = UserWorkoutSerializer(user_workout)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_workout(request, workout_id):
    """закончить тренировку"""
    user_workout = get_object_or_404(
        UserWorkout,
        workout_id=workout_id,
        user=request.user,
        completed_at__isnull=True
    )
    user_workout.completed_at = timezone.now()
    user_workout.save()
    serializer = UserWorkoutSerializer(user_workout)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_workout_history(request):
    """история тренировок пользователя"""
    user_workouts = UserWorkout.objects.filter(user=request.user)
    serializer = UserWorkoutSerializer(user_workouts, many=True)
    return Response(serializer.data)


# Blog related views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blog_list(request):
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def blog_detail(request, id):
    """просмотр поста"""
    blog = get_object_or_404(BlogPost, id=id)
    serializer = BlogPostSerializer(blog)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_blog_post(request):
    """создание нового поста"""
    serializer = BlogPostSerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_blog_post(request, id):
    """обновить пост"""
    blog = get_object_or_404(BlogPost, id=id)

    # Check if user is author
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


# Trainer related views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trainer_list(request):
    """список всех тренеров"""
    trainers = Trainer.objects.all()
    serializer = TrainerSerializer(trainers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trainer_detail(request, id):
    """данные тренера"""
    trainer = get_object_or_404(Trainer, id=id)
    serializer = TrainerSerializer(trainer)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def trainer_creation(request):
    """создать тренера"""
    serializer = TrainerSerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        # serializer.save(user=request.user)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_trainer_profile(request):
    """обновить информацию о тренере"""
    try:
        trainer = request.user.trainer_profile
    except Trainer.DoesNotExist:
        return Response(
            {"error": "User does not have a trainer profile"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TrainerSerializer(
        trainer,
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)