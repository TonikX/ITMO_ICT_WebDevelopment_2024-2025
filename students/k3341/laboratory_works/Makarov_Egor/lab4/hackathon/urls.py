from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TagViewSet, TaskViewSet, TaskResourceLinkViewSet, TaskResourceFileViewSet,
    TeamViewSet, SolutionViewSet, EvaluationViewSet, AnalyticsViewSet
)

router = DefaultRouter()
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"task-resource-links", TaskResourceLinkViewSet, basename="task-resource-links")
router.register(r"task-resource-files", TaskResourceFileViewSet, basename="task-resource-files")
router.register(r"teams", TeamViewSet, basename="teams")
router.register(r"solutions", SolutionViewSet, basename="solutions")
router.register(r"evaluations", EvaluationViewSet, basename="evaluations")
router.register(r"analytics", AnalyticsViewSet, basename="analytics")

urlpatterns = [
    path("", include(router.urls)),
]
