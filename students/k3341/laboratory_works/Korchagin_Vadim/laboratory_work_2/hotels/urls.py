from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    # Вход пользователя
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # Выход пользователя
    path('logout/', LogoutView.as_view(), name='logout'),
    # Регистрация нового пользователя
    path('register/', views.register, name='register'),
    # Просмотр списка комнат
    path('rooms/', views.room_list, name='room_list'),
    # Просмотр деталей комнаты
    path('room/<int:pk>/', views.room_detail, name='room_detail'),
    # Создание бронирования комнаты
    path('room/<int:room_pk>/book/', views.booking_create, name='booking_create'),
    # Список бронирований пользователя
    path('bookings/', views.booking_list, name='booking_list'),
    # Редактирование бронирования
    path('booking/<int:pk>/edit/', views.booking_update, name='booking_update'),
    # Удаление бронирования
    path('booking/<int:pk>/delete/', views.booking_delete, name='booking_delete'),
    # Добавление отзыва к бронированию
    path('booking/<int:booking_id>/add_review/', views.add_review, name='add_review'),
    # Просмотр гостей за последний месяц
    path('recent_guests/', views.recent_guests, name='recent_guests'),
]