from django.urls import path
from .views import *

app_name = "school_app"

urlpatterns = [
    path('teachers/', TeacherAPIView.as_view(), name='teachers_list'), #список учителей
    path('students/', StudentAPIView.as_view(), name='students_list'), #список учеников
    path('classes/', ClassAPIView.as_view(), name='classes_list'), #список класов
    path('subjects/', SubjectsAPIView.as_view(), name='subjects_list'), #список учителей
    path('classrooms/', ClassroomsAPIView.as_view(), name='classrooms_list'), #список учителей
    path('add_teacher/', AddTeacherView.as_view(), name='add_teacher'), #добавление учителя
    path('add_student/', AddStudentView.as_view(), name='add_student'), #добавление ученика
    path('add_grades/', AddGradesView.as_view(), name='add_grades'), #добавление оценки
    # path('teacher_subjects/', TeacherSubjectView.as_view(), name='teacher_subjects'),
    path('grades/', GradeListView.as_view(), name='grades'),
    path('delete_grade/<int:pk>/', DeleteGradeView.as_view(), name='delete_grade'),
    path('delete_teacher/<int:pk>/', DeleteTeacherView.as_view(), name='delete_teacher'), #удаление учителя
    path('delete_student/<int:pk>/', DeleteStudentView.as_view(), name='delete_student'), #удаление ученик
    path('update_teacher/<int:pk>/', UpdateTeacherView.as_view(), name='update_teacher'), #обновление данных учителя
    path('update_student/<int:pk>/', UpdateStudentView.as_view(), name='update_student'), #обновление данных ученика
    path('update_grade/<int:pk>/', UpdateGradeView.as_view(), name='update_grade'), #обновление оценок
    path('schedule/', ScheduleManagementView.as_view(), name='schedule_list_create'),  #добавление предмета
    path('schedule/<int:pk>/', ScheduleManagementView.as_view(), name='schedule_update_delete'), #обновление/удаление занятия
    path('class-report/<int:class_id>/', ClassReportView.as_view(), name='class_report'), #отчёт об успеваемости класса
    path('teachers-per-subject/', TeachersPerSubject.as_view(), name='teachers_per_subject'), #количество учителей для каждого предмета
    path('students-per-class/<str:class_name>/<str:gender>/', StudentsPerClassGender.as_view(), name='students_per_class_gender'), #количество учеников в классе
    path('classrooms/<str:is_profile>/', ClassroomTypeCount.as_view(), name='classroom_type_count'), #количество проф/непроф классов
    path('schedule/<str:class_name>/<str:day>/<str:lesson_time>/', ClassScheduleAPIView.as_view(), name='class_schedule'), #Какой предмет будет в заданном классе, в заданный день недели на заданном уроке
    path('teacher_subject/', TeacherSubjectView.as_view(), name='create_teacher_subject'),
    path('add_teacher_subject/', TeacherSubjectAddView.as_view(), name='add_teacher_subject'),
    path('update_teacher_subject/<int:pk>/', UpdateTeacherSubjectView.as_view(), name='update_teacher_subject'),
    path('delete_teacher_subject/<int:pk>/', DeleteTeacherSubjectView.as_view(), name='delete_teacher_subject'),
    path('student_class/', StudentClassManagementView.as_view(), name='student_class_list'),
    path('add_student_class/', StudentClassAddView.as_view(), name='student_class_detail'),
    path('update_student_class/<int:pk>/', UpdateStudentClassView.as_view(), name='update_student_class'),
    path('delete_student_class/<int:pk>/', DeleteStudentClassView.as_view(), name='delete_student_class'),
    path('studentsfull/', StudentFullListView.as_view(), name='studentsfull'),
    path('teachersfull/', TeacherFullListView.as_view(), name='teachersfull')
]