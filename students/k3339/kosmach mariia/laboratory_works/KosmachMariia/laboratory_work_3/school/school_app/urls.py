from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    path('teachers/all/', TeacherListView.as_view(), name='teacher_list'),
    path('teachers/<int:pk>/', TeacherRetrieveView.as_view(), name='teacher_detail'),
    path('teachers/create/', TeacherCreateView.as_view(), name='teacher_create'),
    path('teachers/update/<int:pk>/', TeacherUpdateView.as_view(), name='teacher_update'),
    path('teachers/delete/<int:pk>/', TeacherDeleteView.as_view(), name='teacher_delete'),

    path('cabinets/all/', CabinetListView.as_view(), name='cabinet_list'),
    path('cabinets/<int:pk>/', CabinetRetrieveView.as_view(), name='cabinet_detail'),
    path('cabinets/create/', CabinetCreateView.as_view(), name='cabinet_create'),
    path('cabinets/update/<int:pk>/', CabinetUpdateView.as_view(), name='cabinet_update'),
    path('cabinets/delete/<int:pk>/', CabinetDeleteView.as_view(), name='cabinet_delete'),

    path('classes/all/', ClassListView.as_view(), name='class_list'),
    path('classes/<int:pk>/', ClassRetrieveView.as_view(), name='class_detail'),
    path('classes/create/', ClassCreateView.as_view(), name='class_create'),
    path('classes/update/<int:pk>/', ClassUpdateView.as_view(), name='class_update'),
    path('classes/delete/<int:pk>/', ClassDeleteView.as_view(), name='class_delete'),

    path('students/all/', StudentListView.as_view(), name='student_list'),
    path('students/<int:pk>/', StudentRetrieveView.as_view(), name='student_detail'),
    path('students/create/', StudentCreateView.as_view(), name='student_create'),
    path('students/update/<int:pk>/', StudentUpdateView.as_view(), name='student_update'),
    path('students/delete/<int:pk>/', StudentDeleteView.as_view(), name='student_delete'),

    path('schedules/all/', ScheduleListView.as_view(), name='schedule_list'),
    path('schedules/<int:pk>/', ScheduleRetrieveView.as_view(), name='schedule_detail'),
    path('schedules/create/', ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedules/update/<int:pk>/', ScheduleUpdateView.as_view(), name='schedule_update'),
    path('schedules/delete/<int:pk>/', ScheduleDeleteView.as_view(), name='schedule_delete'),

    path('teachings/all/', TeachingListView.as_view(), name='teaching_list'),
    path('teachings/<int:pk>/', TeachingRetrieveView.as_view(), name='teaching_detail'),
    path('teachings/create/', TeachingCreateView.as_view(), name='teaching_create'),
    path('teachings/update/<int:pk>/', TeachingUpdateView.as_view(), name='teaching_update'),
    path('teachings/delete/<int:pk>/', TeachingDeleteView.as_view(), name='teaching_delete'),

    path('subjects/all/', SubjectListView.as_view(), name='subject_list'),
    path('subjects/<int:pk>/', SubjectRetrieveView.as_view(), name='subject_detail'),
    path('subjects/create/', SubjectCreateView.as_view(), name='subject_create'),
    path('subjects/update/<int:pk>/', SubjectUpdateView.as_view(), name='subject_update'),
    path('subjects/delete/<int:pk>/', SubjectDeleteView.as_view(), name='subject_delete'),

    path('grades/all/', GradeListView.as_view(), name='grade_list'),
    path('grades/<int:pk>/', GradeRetrieveView.as_view(), name='grade_detail'),
    path('grades/create/', GradeCreateView.as_view(), name='grade_create'),
    path('grades/update/<int:pk>/', GradeUpdateView.as_view(), name='grade_update'),
    path('grades/delete/<int:pk>/', GradeDeleteView.as_view(), name='grade_delete'),

    path('auth/', include('djoser.urls')),
    path('auth/token', obtain_auth_token, name='token'),
    path('logout', LogOut.as_view()),

    path('students_by_grades/<str:grade>/', SpecialStudentListView.as_view(), name='list_of_students'),
]