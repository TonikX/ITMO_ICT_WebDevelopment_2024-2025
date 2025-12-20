# urls.py
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    # Аутентификация
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('me/', views.CurrentUserAPIView.as_view(), name='current-user'),

    # 1. Кабинеты
    path('classrooms/', views.ClassRoomListAPIView.as_view(), name='classrooms-list'),

    # 2. Преподаватели
    path('teachers/', views.TeachersAPIView.as_view(), name='active-teachers'),
    path('teacher/create/', views.TeacherCreateAPIView.as_view(), name='teacher-create'),
    path('teacher/delete/<int:pk>/', views.TeacherDeleteAPIView.as_view(), name='teacher-delete'),
    path('teacher/update/<int:pk>/', views.TeacherUpdateAPIView.as_view(), name='teacher-update'),

    # 3. Группы
    path('groups/', views.GroupsByCourseAPIView.as_view(), name='all-groups'),
    path('groups/course/<int:course>/', views.GroupsByCourseAPIView.as_view(), name='groups-by-course'),
    path('groups/<int:group_id>/detail/', views.GroupDetailWithCuratorAPIView.as_view(), name='group-detail'),
    path('groups/<int:group_id>/nested/', views.GroupDetailWithNestedAPIView.as_view(), name='group-detail-nested'),

    # 4. Студенты
    path('students/search/', views.StudentSearchAPIView.as_view(), name='student-search'),
    path('student/create/', views.StudentCreateAPIView.as_view(), name='student-create'),
    path('student/update/<int:pk>/', views.StudentUpdateAPIView.as_view(), name='student-update'),
    path('student/delete/<int:pk>/', views.StudentDeleteAPIView.as_view(), name='student-delete'),
    path('groups/<int:group_id>/students/', views.StudentsByGroupAPIView.as_view(), name='students-by-group'),
    path('students/<int:student_id>/stats/', views.StudentStatsAPIView.as_view(), name='student-stats'),

    # 5. Расписание
    path('schedule/group/<int:group_id>/', views.GroupScheduleAPIView.as_view(), name='group-schedule'),

    # 6. Дисциплины
    path('subjects/course/<int:course>/semester/<int:semester>/',
         views.SubjectsByCourseSemesterAPIView.as_view(), name='subjects-by-course-semester'),
    path('subjects/all/', views.SubjectsAPIView.as_view(), name='subjects-list'),

    # 7. Оценки
    path('students/<int:student_id>/grades/', views.StudentGradesAPIView.as_view(), name='student-grades'),
    path('grades/create/', views.GradeCreateAPIView.as_view(), name='grade-create'),
    path('grades/<int:id>/update/', views.GradeUpdateAPIView.as_view(), name='grade-update'),
    path('grades/<int:id>/delete/', views.GradeDeleteAPIView.as_view(), name='grade-delete'),
]