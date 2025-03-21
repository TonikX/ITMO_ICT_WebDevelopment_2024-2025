from django.urls import path

from school_app.views import TeacherAPIView, TeacherDetailView, HomeTeacherAPIView, StudentAPIView, StudentDetailView, \
    ScheduleAPIView, \
    ScheduleDetailAPIView, SubjectViewByDayAndLessonNumber, \
    TeacherOfSubjectsCountView, TeachersByTeacherInClass, BoysAndGirlsInGroupsView, \
    CountOfSpecializedAndNonSpecializerRoomsView, ReportView, RoomsApiView, RoomsDetailAPIView, GroupAPIView, \
    SubjectAPIVIew, QuarterGradesAPIView, QuarterGradesUpdateView

urlpatterns = [
    path('teachers', TeacherAPIView.as_view()),
    path('teachers/<int:id>', TeacherDetailView.as_view()),
    path('teachers/colleagues', TeachersByTeacherInClass.as_view()),
    path('teachers/home', HomeTeacherAPIView.as_view()),
    path('students', StudentAPIView.as_view()),
    path('students/<int:id>', StudentDetailView.as_view()),
    path('students/<int:id>/grades', QuarterGradesAPIView.as_view()),
    path('grades/<int:pk>', QuarterGradesUpdateView.as_view()),
    path('students/gender', BoysAndGirlsInGroupsView.as_view()),
    path('schedules', ScheduleAPIView.as_view()),
    path('schedules/<int:id>', ScheduleDetailAPIView.as_view()),
    path('schedule/subject', SubjectViewByDayAndLessonNumber.as_view()),
    path('subjects/teachers_count', TeacherOfSubjectsCountView.as_view()),
    path('subjects', SubjectAPIVIew.as_view()),
    path('rooms/profile_base', CountOfSpecializedAndNonSpecializerRoomsView.as_view()),
    path('rooms', RoomsApiView.as_view()),
    path('rooms/<int:id>', RoomsDetailAPIView.as_view()),
    path('groups', GroupAPIView.as_view()),
    path('report', ReportView.as_view())
]
