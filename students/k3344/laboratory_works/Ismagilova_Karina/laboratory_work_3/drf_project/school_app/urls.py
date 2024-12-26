from django.urls import path
from .views import *

urlpatterns = [
    path('students/', StudentListCreateView.as_view()),
    path('students/<int:pk>/', StudentDetailView.as_view()),
    path('teachers/', TeacherListCreateView.as_view()),
    path('teachers/<int:pk>/', TeacherDetailView.as_view()),
    path('grades/', GradeListCreateView.as_view()),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('rooms/', RoomListCreateView.as_view(), name='room-list-create'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('student-schedules/', StudentScheduleListCreateView.as_view(), name='student-schedule-list-create'),
    path('student-schedules/<int:pk>/', StudentScheduleDetailView.as_view(), name='student-schedule-detail'),
    path('rooms/<str:room_number>/day/<str:day>/', SubjectInRoomView.as_view(), name='subject-in-room'),
    path('teachers-per-subject/', TeachersPerSubjectView.as_view(), name='teachers-per-subject'),
    path('gender-count-per-class/', GenderCountPerClassView.as_view(), name='gender-count-per-class'),
    path('room-count/', RoomCountByStatusView.as_view(), name='room-count-by-status'),
    path('teachers-with-same-subjects/<int:teacher_id>/', TeachersWithSameSubjectsView.as_view(), name='teacher'),
    path('student-special-schedules/<int:student_id>/', StudentScheduleView.as_view(), name='student-schedule'),
    path('grades/<int:student_id>/', GradeListView.as_view(), name='student-grades'),
]
