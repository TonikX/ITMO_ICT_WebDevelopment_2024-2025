from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, TeacherViewSet, GradeViewSet, ScheduleViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'schedule', ScheduleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
