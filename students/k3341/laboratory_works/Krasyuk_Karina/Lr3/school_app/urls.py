from django.urls import path

from school_app.serializers import SubjectTeacherCountSerializer
from school_app.views import TeacherAPIView, TeacherDetailView, TeacherUpdateView, TeacherDeleteView, \
    HomeTeacherAPIView, StudentAPIView, StudentDetailView, StudentUpdateView, StudentDeleteView, ScheduleAPIView, \
    ScheduleDetailAPIView, ScheduleUpdateView, ScheduleDeleteView, SubjectViewByDayAndLessonNumber, \
    TeacherOfSubjectsCountView, TeachersByTeacherInClass, BoysAndGirlsInGroupsView, \
    CountOfSpecializedAndNonSpecializerRoomsView, ReportView

urlpatterns = [
    path('teachers', TeacherAPIView.as_view()),
    path('teachers/<int:id>', TeacherDetailView.as_view()),
    path('teachers/<int:id>/update', TeacherUpdateView.as_view()),
    path('teachers/<int:id>/delete', TeacherDeleteView.as_view()),
    path('teachers/colleagues', TeachersByTeacherInClass.as_view()),
    path('teachers/home', HomeTeacherAPIView.as_view()),
    path('students', StudentAPIView.as_view()),
    path('students/<int:id>', StudentDetailView.as_view()),
    path('students/<int:id>/update', StudentUpdateView.as_view()),
    path('students/<int:id>/delete', StudentDeleteView.as_view()),
    path('students/gender', BoysAndGirlsInGroupsView.as_view()),
    path('schedules', ScheduleAPIView.as_view()),
    path('schedules/<int:id>', ScheduleDetailAPIView.as_view()),
    path('schedules/<int:id>/update', ScheduleUpdateView.as_view()),
    path('schedules/<int:id>/delete', ScheduleDeleteView.as_view()),
    path('schedule/subject', SubjectViewByDayAndLessonNumber.as_view()),
    path('subjects/teachers_count', TeacherOfSubjectsCountView.as_view()),
    path('rooms/profile_base', CountOfSpecializedAndNonSpecializerRoomsView.as_view()),
    path('report', ReportView.as_view())
]