# админка Django
from django.contrib import admin

# маршруты
from django.urls import path, include

# разрешения DRF
from rest_framework import permissions

# Swagger документация
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# настройка Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version="v1",
        description="API системы управления библиотекой",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

    # админ панель
    path("admin/", admin.site.urls),

    # API библиотеки
    path("api/", include("library.urls")),

    # регистрация и логин (Djoser)
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),

    # Swagger документация
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
]