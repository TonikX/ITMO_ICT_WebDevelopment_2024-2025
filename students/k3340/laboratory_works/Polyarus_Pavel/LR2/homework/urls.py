from django.urls import path
from . import views

app_name = 'homework'

urlpatterns = [
    path('', views.homework_list, name='list'),
    
    path('<int:pk>/', views.homework_detail, name='detail'),
    path('create/', views.homework_create, name='create'),
    path('<int:pk>/update/', views.homework_update, name='update'),
    path('<int:pk>/delete/', views.homework_delete, name='delete'),
    
    path('<int:pk>/submit/', views.submit_homework, name='submit'),
    path('submissions/', views.submission_list, name='submission_list'),
    path('submissions/<int:pk>/grade/', views.grade_submission, name='grade_submission'),

    path("my-grades/", views.my_grades, name="my_grades"),
    path("grades/", views.grades_table, name="grades_table"),
]