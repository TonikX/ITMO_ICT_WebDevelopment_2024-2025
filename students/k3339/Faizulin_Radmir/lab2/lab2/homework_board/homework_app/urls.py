from . import views
from django.urls import path

urlpatterns = [
    path('homeworks/', views.homework_list, name='homework_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('homeworks/grades/', views.grades_table, name='grades_table'),
    path('homeworks/<int:homework_id>/', views.submit_homework, name='submit_homework'),
]
