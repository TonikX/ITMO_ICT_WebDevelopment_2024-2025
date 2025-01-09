from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('account/', views.account_view, name='account'),
    path('logout/', views.logout_view, name='logout'),
    path('homework/add/', views.add_homework, name='add_homework'),
    path('homework/edit/<int:homework_id>/', views.edit_homework, name='edit_homework'),
    path('homework/delete/<int:homework_id>/', views.delete_homework, name='delete_homework'),
    path('homework/', views.homework_list, name='homework_list'),
    path('homework/submit/<int:homework_id>/', views.submit_homework, name='submit_homework'),
    path('grades/', views.grade_table, name='grade_table'),
    path('submission/grade/<int:submission_id>/', views.grade_submission, name='grade_submission'),
    path('submissions/', views.submission_list, name='submission_list'),
    path('submission/edit/<int:submission_id>/', views.edit_submission, name='edit_submission'),
    path('submission/delete/<int:submission_id>/', views.delete_submission, name='delete_submission'),
]
