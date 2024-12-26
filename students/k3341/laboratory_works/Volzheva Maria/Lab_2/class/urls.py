from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_welcome),
    path('registration/', views.RegistrationView.as_view()),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('home/', views.get_home, name='home'),
    path('homework/<int:pk>/', views.get_homework, name='get_homework'),
    path('homework/<int:pk>/new_submission/', views.create_submission_),
    path('submission/<int:pk>/', views.get_submission),
    path('grades_for_teacher/', views.grades_by_subject_per_class, name='grades_by_subject_per_class'),
    path('submissions/without-grades/', views.submissions_without_grades, name='submissions_without_grades'),
    path('submissions/grade/<int:pk>/', views.grade_submission, name='grade_submission'),


]
