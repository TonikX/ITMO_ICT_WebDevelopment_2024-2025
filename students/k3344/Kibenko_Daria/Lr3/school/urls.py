from django.urls import path, include

urlpatterns = [
    path('auth/', include('djoser.urls')),  # Основные маршруты для регистрации и авторизации
    path('auth/token/', include('djoser.urls.authtoken')),  # Токен аутентификации
    path('auth/users/me/', include('djoser.urls.users')),  # Получение информации о текущем пользователе
]
