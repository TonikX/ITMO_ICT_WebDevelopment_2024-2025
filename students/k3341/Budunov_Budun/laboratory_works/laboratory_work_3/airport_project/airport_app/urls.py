from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

router = DefaultRouter()
router.register(r'airline', AirlineViewSet)
router.register(r'airport', AirportViewSet)
router.register(r'route', RouteViewSet)
router.register(r'transit', TransitViewSet)
router.register(r'airplane_model', AirplaneModelViewSet)
router.register(r'airplane', AirplaneViewSet)
router.register(r'airplane_maintenance', AirplaneMaintenanceViewSet)
router.register(r'employee', EmployeeViewSet)
router.register(r'crew', CrewViewSet)
router.register(r'crew_member', CrewMemberViewSet)
router.register(r'flight', FlightViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls')),  # Includes djoser's URLs for user management (registration, login, etc.)
    path('api/auth/', include('djoser.urls.jwt')),  # Includes djoser's JWT URLs (obtain, refresh, verify tokens)
    path('login/', LoginUserView.as_view(), name='login'),
    path('user/<int:pk>/avatar/', UserAvatarUpdateView.as_view(), name='user_avatar_update'),
]
