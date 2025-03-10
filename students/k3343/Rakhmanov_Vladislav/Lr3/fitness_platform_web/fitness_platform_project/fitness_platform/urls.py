from django.urls import path
from . import views

app_name = "fitness_platform"

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/create/', views.UserCreateAPIView.as_view(), name='user-create'),
    path('current-user/', views.CurrentUserView.as_view(), name='current-user'),

    path('progress/', views.ProgressListCreateView.as_view(), name='progress-list-create'),
    path('progress/<int:pk>/', views.ProgressDetailView.as_view(), name='progress-detail'),

    path('workout-plans/', views.WorkoutPlanListCreateView.as_view(), name='workout-plan-list-create'),
    path('workout-plans/<int:pk>/', views.WorkoutPlanDetailView.as_view(), name='workout-plan-detail'),

    path('workouts/', views.WorkoutListCreateView.as_view(), name='workout-list-create'),
    path('workouts/<int:pk>/', views.WorkoutDetailView.as_view(), name='workout-detail'),

    path('blog-posts/', views.BlogPostListCreateView.as_view(), name='blog-post-list-create'),
    path('blog-posts/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog-post-detail'),
]
