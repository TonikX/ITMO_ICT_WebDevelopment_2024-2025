from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from head_teacher_app import views

urlpatterns = [
    path("rooms/", views.RoomListCreateAPIView.as_view(), name="room-list-create"),
    path("rooms/<int:pk>/", views.RoomDetailAPIView.as_view(), name="room-detail"),
    path("teachers/", views.TeacherListCreateAPIView.as_view(), name="teacher-list-create"),
    path("teachers/<int:pk>/", views.TeacherDetailAPIView.as_view(), name="teacher-detail"),
    path("subjects/", views.SubjectListCreateAPIView.as_view(), name="subject-list-create"),
    path("subjects/<int:pk>/", views.SubjectDetailAPIView.as_view(), name="subject-detail"),
    path("classes/", views.ClassListCreateAPIView.as_view(), name="classes-list-create"),
    path("classes/<int:pk>/", views.ClassDetailAPIView.as_view(), name="classes-detail"),
    path("students/", views.StudentListCreateAPIView.as_view(), name="students-list-create"),
    path("students/<int:pk>/", views.StudentDetailAPIView.as_view(), name="students-detail"),
    path("schedule/", views.ScheduleListCreateAPIView.as_view(), name="schedule-list-create"),
    path("schedule/<int:pk>/", views.ScheduleDetailAPIView.as_view(), name="schedule-detail"),
    path("grades/", views.GradeListCreateAPIView.as_view(), name="grades-list-create"),
    path("grades/<int:pk>/", views.GradeDetailAPIView.as_view(), name="grades-detail"),
    path("schedule/subject/", views.ScheduleByClassAPIView.as_view(), name="subject-by-class"),
    path("subjects/teacher-count/", views.TeachersPerSubjectAPIView.as_view(), name="teachers-per-subject"),
    path("classes/gender-count/", views.GenderCountPerClassAPIView.as_view(), name="gender-count-per-class"),
    path("rooms/count/", views.RoomCountAPIView.as_view(), name="room-count"),
    path("classes/performance-report/", views.ClassPerformanceReportAPIView.as_view(), name="class-performance-report"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"), 
]
