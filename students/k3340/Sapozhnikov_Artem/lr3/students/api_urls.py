from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, SchoolClassViewSet, GradeViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'classes', SchoolClassViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = router.urls
