from django.urls import path, re_path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('login-user/', views.login_user, name='login-user'),
    path('register-user/', views.register_user, name='register-user'),
    path('homework-list/', views.homework_list, name='homework-list'),
    path('teachers-list/', views.teachers_list, name='teachers-list'),
    path('homework-submit/<int:task_id>/', views.homework_submit, name='homework-submit'),
    path('teachers-submit/<int:grade_id>/', views.teachers_submit, name='teachers-submit'),
    path('teachers-create/', views.teachers_create, name='teachers-create'),
    path('grade-table/', views.grade_table, name='grade-table'),
    path('logout-user/', views.logout_user, name='logout-user'),
    re_path(r'^.*$', lambda request: redirect('login-user')),
]
