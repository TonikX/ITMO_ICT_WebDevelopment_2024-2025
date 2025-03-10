from django.urls import path, include
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, WorkoutViewSet, BlogViewSet

app_name = 'fitness_app'
router = DefaultRouter()
router.register(r'account', AccountViewSet, basename='account')
router.register(r'workouts', WorkoutViewSet, basename='workouts')
router.register(r'blogs', BlogViewSet, basename='blogs')

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API documentation",
        contact=openapi.Contact(email="contact@yourapi.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path('api/v1/', include(router.urls))],
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
