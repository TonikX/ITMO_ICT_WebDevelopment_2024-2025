from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="conference API",
        default_version='v1',
        description="Visualization of conference API working",
        contact=openapi.Contact(email="farbikredemy@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("conference_api.urls")),
    path('', include("participation_api.urls")),
    path('', include("auth_api.urls")),
    path('work/', include("work_api.urls")),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
