from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger/OpenAPI схема
schema_view = get_schema_view(
    openapi.Info(
        title="College Management System API",
        default_version='v1.0',
        description="API системы управления учебной частью колледжа",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@college.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Router для ViewSets
router = DefaultRouter()
router.register(r'groups', views.GroupViewSet, basename='group')
router.register(r'classrooms', views.ClassroomViewSet, basename='classroom')
router.register(r'teachers', views.TeacherViewSet, basename='teacher')
router.register(r'subjects', views.SubjectViewSet, basename='subject')
router.register(r'students', views.StudentViewSet, basename='student')
router.register(r'schedules', views.ScheduleViewSet, basename='schedule')
router.register(r'grades', views.GradeViewSet, basename='grade')

urlpatterns = [
    # эндпоинты
    path('', include(router.urls)),

    # запросы из задания
    path('queries/schedule/', views.schedule_query, name='schedule_query'),
    path('queries/teachers-by-group/', views.teachers_by_group, name='teachers_by_group'),
    path('queries/groups-by-subject-teacher/', views.groups_by_subject_teacher, name='groups_by_subject_teacher'),
    path('queries/group-schedule/', views.group_schedule, name='group_schedule'),
    path('queries/students-by-course/<int:course>/', views.students_by_course, name='students_by_course'),
    path('queries/group-performance/', views.group_performance_report, name='group_performance_report'),

    # эндпоинты для статистики
    path('statistics/dashboard/', views.dashboard_stats, name='dashboard_stats'),
    path('statistics/courses/', views.course_statistics, name='course_statistics'),

    # документация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]