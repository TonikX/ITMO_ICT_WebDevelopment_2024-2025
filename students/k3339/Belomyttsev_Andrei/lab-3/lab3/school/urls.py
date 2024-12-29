from school.views import TeacherViewSet, StudentViewSet, SubjectViewSet, MarkViewSet, LessonViewSet, GradeViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter() # SimpleRouter
router.register(r'teacher', TeacherViewSet)
router.register(r'student', StudentViewSet)
router.register(r'subject', SubjectViewSet)
router.register(r'mark', MarkViewSet)
router.register(r'lesson', LessonViewSet)
router.register(r'grade', GradeViewSet)

urlpatterns = [
  path('', include(router.urls)),
  path('auth/', include('djoser.urls')),
  path('auth/', include('djoser.urls.authtoken')),
]