from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
    path('login/', views.CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('homeworks/', views.HomeworkListView.as_view(), name='homework_list'),
    path('student/homeworks/', views.StudentHomeworkListView.as_view(), name='student_homeworks'),
    path('homeworks/create/', views.HomeworkCreateView.as_view(), name='homework_create'),
    path('homeworks/<int:homework_id>/submit/', views.SubmissionCreateView.as_view(), name='submit_homework'),
    path('homeworks/list/submissions/', views.SubmissionListView.as_view(), name='submission_list'),
    path('homeworks/submission/<int:submission_id>/grade/', views.SubmissionGradeView.as_view(), name='grade_submission'),
    path('subjects/add/', views.SubjectCreateView.as_view(), name='add_subject'),
    path('subjects/<int:pk>/edit/', views.SubjectUpdateView.as_view(), name='edit_subject'),
    path('grades/admin/', views.AdminGradeTableView.as_view(), name='admin_grade_table'),
    path('grades/student/', views.StudentGradeTableView.as_view(), name='student_grade_table')    
    ]