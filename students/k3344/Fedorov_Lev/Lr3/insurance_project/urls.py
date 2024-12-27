from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from insurance.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('insurance/', include('insurance.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='swagger-json'),
    path('swagger.yaml/', schema_view.without_ui(cache_timeout=0), name='swagger-yaml'),
]