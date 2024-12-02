from django.shortcuts import render
from rest_framework.generics import ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *

# Пользователи
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreateView(APIView):
    def post(self, request):
        user_data = request.data
        serializer = UserSerializer(data=user_data)

        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save() 
            return Response(
                {"Success": f"User '{user_saved.name}' created successfully."}
            )

class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Профили
class ProfileListAPIView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileCreateAPIView(APIView):
    def post(self, request):
        profile_data = request.data
        serializer = ProfileSerializer(data=profile_data)

        if serializer.is_valid(raise_exception=True):
            profile_saved = serializer.save()
            return Response(
                {"Success": f"Profile for {profile_saved.user.name} created successfully."}
            )

class ProfileUpdateAPIView(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDeleteAPIView(DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# Тренировки
class WorkoutListAPIView(ListAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

class WorkoutCreateAPIView(APIView):
    def post(self, request):
        workout_data = request.data
        serializer = WorkoutSerializer(data=workout_data)
        if serializer.is_valid(raise_exception=True):
            workout_saved = serializer.save()
            return Response({"Success": f"Workout '{workout_saved.title}' created successfully."})

class WorkoutUpdateAPIView(UpdateAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

class WorkoutDeleteAPIView(DestroyAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer


# Планы тренировок
class WorkoutPlanListAPIView(ListAPIView):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer

class WorkoutPlanCreateAPIView(APIView):
    def post(self, request):
        workout_plan_data = request.data
        serializer = WorkoutPlanSerializer(data=workout_plan_data)

        if serializer.is_valid(raise_exception=True):
            workout_plan_saved = serializer.save()
            return Response(
                {"Success": f"Workout Plan for {workout_plan_saved.user.name} created successfully."}
            )

class WorkoutPlanUpdateAPIView(UpdateAPIView):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer

class WorkoutPlanDeleteAPIView(DestroyAPIView):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer


# Посты блога
class BlogPostListAPIView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class BlogPostCreateAPIView(APIView):
    def post(self, request):
        blogpost_data = request.data
        serializer = BlogPostSerializer(data=blogpost_data)
        if serializer.is_valid(raise_exception=True):
            blogpost_saved = serializer.save()
            return Response({"Success": f"BlogPost '{blogpost_saved.title}' created successfully."})

class BlogPostUpdateAPIView(UpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class BlogPostDeleteAPIView(DestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


# Прогресс-трекинг
class ProgressTrackingListAPIView(ListAPIView):
    queryset = ProgressTracking.objects.all()
    serializer_class = ProgressTrackingSerializer

class ProgressTrackingCreateAPIView(APIView):
    def post(self, request):
        progress_tracking_data = request.data
        serializer = ProgressTrackingSerializer(data=progress_tracking_data)

        if serializer.is_valid(raise_exception=True):
            progress_tracking_saved = serializer.save()
            return Response(
                {"Success": f"Progress Tracking for {progress_tracking_saved.user.name} created successfully."}
            )

class ProgressTrackingUpdateAPIView(UpdateAPIView):
    queryset = ProgressTracking.objects.all()
    serializer_class = ProgressTrackingSerializer

class ProgressTrackingDeleteAPIView(DestroyAPIView):
    queryset = ProgressTracking.objects.all()
    serializer_class = ProgressTrackingSerializer


# Вся информация о пользователе
class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer