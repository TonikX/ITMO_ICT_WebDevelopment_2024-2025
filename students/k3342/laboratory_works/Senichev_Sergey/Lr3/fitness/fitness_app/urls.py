from django.urls import path
from . import views

app_name = 'fitness_app'

urlpatterns = [
    path('account/', views.account_info, name='account_info'),
    path('account/workouts/', views.user_workout_history, name='user_workouts'),

    path('workouts/', views.workout_list, name='workout_list'),
    path('workouts/create/', views.submit_workout, name='create_workout'),
    path('workouts/<int:id>/', views.workout_detail, name='workout_detail'),
    path('workouts/submit/', views.submit_workout, name='submit_workout'),

    path('workouts/<int:workout_id>/start/', views.start_workout, name='workout_detail'),
    path('workouts/<int:workout_id>/complete/', views.complete_workout, name='workout_detail'),

    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:id>/', views.blog_detail, name='blog_detail'),
    path('blogs/create/', views.create_blog_post, name='create_blog'),

    path('trainers/', views.trainer_list, name='trainer_list'),
    path('trainers/<int:id>/', views.trainer_detail, name='trainer_detail'),
    path('trainers/create/', views.trainer_creation, name='trainer_creation'),
]