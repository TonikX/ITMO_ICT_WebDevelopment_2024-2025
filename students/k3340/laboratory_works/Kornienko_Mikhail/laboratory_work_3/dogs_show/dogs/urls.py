from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OwnerViewSet, DogViewSet, ShowViewSet, ParticipationViewSet, ExpertViewSet, GradeViewSet

router = DefaultRouter()
router.register('owners', OwnerViewSet)
router.register('dogs', DogViewSet)
router.register('shows', ShowViewSet)
router.register('participations', ParticipationViewSet)
router.register('experts', ExpertViewSet)
router.register('grades', GradeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
