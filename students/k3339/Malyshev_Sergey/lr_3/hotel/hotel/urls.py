from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api_urls')), # API

    path('auth/', include('djoser.urls')),               # базовые эндпоинты Djoser
    path('auth/', include('djoser.urls.authtoken')),     # эндпоинты
]