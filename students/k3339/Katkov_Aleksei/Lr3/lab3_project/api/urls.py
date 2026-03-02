from django.urls import path
from .views import *

urlpatterns = [

    # Category
    path('categories/', CategoryListCreateView.as_view()),
    path('categories/<int:pk>/', CategoryDetailView.as_view()),
    path('categories/full/', CategoryWithTasksView.as_view()),

    # Task
    path("tasks/", TaskListCreateView.as_view()),
    path('tasks/<int:pk>/', TaskDetailView.as_view()),
    path('tasks/full/', TaskFullInfoView.as_view()),
    path('tags/', TagListCreateView.as_view()),
    path('tags/<int:pk>/', TagDetailView.as_view()),

]
