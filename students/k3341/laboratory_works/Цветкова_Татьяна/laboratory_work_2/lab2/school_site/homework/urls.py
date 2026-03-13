from django.urls import path
from . import views

urlpatterns = [
    path('', views.homework_list, name='homework_list'),
    path('submit/<int:homework_id>/', views.submit_homework, name='submit_homework'),
    path('grades/', views.grade_table, name='grade_table'),
]
