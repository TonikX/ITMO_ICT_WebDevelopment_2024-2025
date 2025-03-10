from django.urls import path, include
from rest_framework import permissions

from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter

app_name = 'fitness_app'


urlpatterns = [
    path('account/', views.account_info, name='account_info'),
    path('account/update/', views.update_account_info, name='update_account_info'),
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
]
