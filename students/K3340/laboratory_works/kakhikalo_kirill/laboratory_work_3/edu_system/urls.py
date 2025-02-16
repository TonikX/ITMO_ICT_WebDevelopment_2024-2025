from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EducationProgramViewSet,
    AcademicDisciplineViewSet,
    ProgramElementViewSet,
    GroupViewSet,
    StudentViewSet,
    ClassroomViewSet,
    TeacherViewSet,
    ClassSessionViewSet,
    TeachingPermitViewSet,
    ResultViewSet
)

router = DefaultRouter()
router.register('educationprograms', EducationProgramViewSet)
router.register('academicdisciplines', AcademicDisciplineViewSet)
router.register('programelements', ProgramElementViewSet)
router.register('groups', GroupViewSet)
router.register('students', StudentViewSet)
router.register('classrooms', ClassroomViewSet)
router.register('teachers', TeacherViewSet)
router.register('classsessions', ClassSessionViewSet)
router.register('teachingpermits', TeachingPermitViewSet)
router.register('results', ResultViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]