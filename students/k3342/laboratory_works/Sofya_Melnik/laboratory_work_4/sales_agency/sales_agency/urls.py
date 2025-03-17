from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Админ-панель
    path('admin/', admin.site.urls),

    # Основное API приложения
    path('', include('sales_agency_app.urls')),

    # --- Swagger/OpenAPI ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # --- Аутентификация ---
    path('api/auth/', include('djoser.urls')),  # эндпоинты Djoser (регистрация, изменение пароля)
    path('api/auth/', include('djoser.urls.jwt')),  # JWT-аутентификация (токены)

    # Встроенная аутентификация DRF
    path('api-auth/', include("rest_framework.urls")),
]
