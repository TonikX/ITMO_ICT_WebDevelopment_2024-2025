from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HabitatViewSet, DepartmentViewSet, BuildingViewSet,
    EnclosureViewSet, StaffViewSet, AnimalViewSet,
    FeedingRationTypeViewSet, FeedingRationViewSet,
    ZooViewSet, WinteringPlaceViewSet, FeedingHistoryViewSet,
    CaretakerAssignmentViewSet, VeterinarianAssignmentViewSet,
    TransferHistoryViewSet
)

router = DefaultRouter()
router.register(r'habitats', HabitatViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'buildings', BuildingViewSet)
router.register(r'enclosures', EnclosureViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'animals', AnimalViewSet)
router.register(r'feeding-ration-types', FeedingRationTypeViewSet)
router.register(r'feeding-rations', FeedingRationViewSet)
router.register(r'zoos', ZooViewSet)
router.register(r'wintering-places', WinteringPlaceViewSet)
router.register(r'feeding-histories', FeedingHistoryViewSet)
router.register(r'caretaker-assignments', CaretakerAssignmentViewSet)
router.register(r'veterinarian-assignments', VeterinarianAssignmentViewSet)
router.register(r'transfer-histories', TransferHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]