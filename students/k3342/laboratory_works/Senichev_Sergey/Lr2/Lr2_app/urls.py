from django.urls import path
from . import views

app_name = 'homework'

urlpatterns = [
    path('account/', views.account_info, name='account_info'),
    path('account/register/', views.register, name='register'),
    path('account/login/', views.login_view, name='login'),
    path('account/logout/', views.logout_view, name='logout'),

    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:id>/', views.task_detail, name='task_detail'),
    path('tasks/submit/', views.submit_task, name='submit_task'),
    path('tasks/pending/', views.pending_tasks, name='pending_tasks'),

    path('grades/', views.my_grades, name='my_grades'),

    path('grades/all/', views.admin_dashboard, name='admin_dashboard'),
]
