from django.urls import path
from .views import *

urlpatterns = [
    # User
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),

    # Профили
    path('profiles/', ProfileListAPIView.as_view(), name='profile-list'),
    path('profiles/create/', ProfileCreateAPIView.as_view(), name='profile-create'),
    path('profiles/<int:pk>/update/', ProfileUpdateAPIView.as_view(), name='profile-update'),
    path('profiles/<int:pk>/delete/', ProfileDeleteAPIView.as_view(), name='profile-delete'),

    # Тренировки
    path('workouts/', WorkoutListAPIView.as_view(), name='workout-list'),
    path('workouts/create/', WorkoutCreateAPIView.as_view(), name='workout-create'),
    path('workouts/<int:pk>/update/', WorkoutUpdateAPIView.as_view(), name='workout-update'),
    path('workouts/<int:pk>/delete/', WorkoutDeleteAPIView.as_view(), name='workout-delete'),

    # Посты блога
    path('blogposts/', BlogPostListAPIView.as_view(), name='blogpost-list'),
    path('blogposts/create/', BlogPostCreateAPIView.as_view(), name='blogpost-create'),
    path('blogposts/<int:pk>/update/', BlogPostUpdateAPIView.as_view(), name='blogpost-update'),
    path('blogposts/<int:pk>/delete/', BlogPostDeleteAPIView.as_view(), name='blogpost-delete'),

    # WorkoutPlan
    path('workout-plans/', WorkoutPlanListAPIView.as_view(), name='workout-plan-list'),
    path('workout-plans/create/', WorkoutPlanCreateAPIView.as_view(), name='workout-plan-create'),
    path('workout-plans/<int:pk>/update/', WorkoutPlanUpdateAPIView.as_view(), name='workout-plan-update'),
    path('workout-plans/<int:pk>/delete/', WorkoutPlanDeleteAPIView.as_view(), name='workout-plan-delete'),

    # ProgressTracking
    path('progress-tracking/', ProgressTrackingListAPIView.as_view(), name='progress-tracking-list'),
    path('progress-tracking/create/', ProgressTrackingCreateAPIView.as_view(), name='progress-tracking-create'),
    path('progress-tracking/<int:pk>/update/', ProgressTrackingUpdateAPIView.as_view(), name='progress-tracking-update'),
    path('progress-tracking/<int:pk>/delete/', ProgressTrackingDeleteAPIView.as_view(), name='progress-tracking-delete'),
]
