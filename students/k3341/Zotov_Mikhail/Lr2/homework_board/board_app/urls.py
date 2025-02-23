from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('logout/', views.logout_user),
    path('grades/', views.show_grades),
    path('subjects/', views.show_all_subjects_specific_group),
    path('groups/', views.AllGroups.as_view()),
    path('groups/<int:group_id>/', views.group_detail),
    path('homeworks/', views.show_homeworks, name='homeworks'),
    path('homework/submit/<int:homework_id>/', views.submit_homework, name='submit_homework'),
    path('view_submissions/', views.view_submissions, name='view_submissions'),
    path('grade_homework/<int:submission_id>/', views.grade_homework, name='grade_homework'),
]
