from django.urls import path
from .views import (
    main,
    register,
    user_login,
    account_view,
    logout_view,
    add_homework,
    edit_homework,
    delete_homework,
    homework_list,
    submission_list,
    submit_homework,
    edit_submission,
    delete_submission,
    grade_submission,
    student_grade_table, student_submission_list
)

urlpatterns = [
    path('', main, name='main'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('account/', account_view, name='account'),
    path('logout/', logout_view, name='logout'),

    path('homeworks/submit/<int:homework_id>/', submit_homework, name='submit_homework'),
    path('homeworks/', homework_list, name='homework_list'),
    path('homeworks/add/', add_homework, name='add_homework'),
    path('homeworks/edit/<int:homework_id>/', edit_homework, name='edit_homework'),
    path('homeworks/delete/<int:homework_id>/', delete_homework, name='delete_homework'),

    path('submissions/', submission_list, name='submission_list'),
    path('submissions/student/', student_submission_list, name='student_submission_list'),
    path('submissions/edit/<int:submission_id>/', edit_submission, name='edit_submission'),
    path('submissions/delete/<int:submission_id>/', delete_submission, name='delete_submission'),

    path('submission/grade/<int:submission_id>/', grade_submission, name='grade_submission'),
    path('grades/', student_grade_table, name='student_grade_table'),
]
