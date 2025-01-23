from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *

urlpatterns = [
    # Пользователь
    path('register/', views.register, name='register'),  # Регистрация 
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Вход
    path('logout/', views.logout_view, name='logout'),  # Выход

    # Рейсы
    path('flights/', FlightListView.as_view(), name='flights'),  # Список

    # Резервирование мест
    path('flights/<int:flight_id>/reserve/', ReservationCreateView.as_view(), name='reserve_form'),  # Создание 
    path('reserve/', ReservationListView.as_view(), name='reservation_list'),  # Список 
    path('reservation/<int:pk>/update/', ReservationUpdateView.as_view(), name='reservation_update'), # обновление
    path('reservation/<int:pk>/delete/', ReservationDeleteView.as_view(), name='reservation_delete'), # Удаление

    # Отзывы о рейсах
    path('flights/<int:flight_id>/reviews/create', ReviewCreateView.as_view(), name='review_form'),
    path('flights/<int:flight_id>/reviews/', ReviewListView.as_view(), name='review_form'),

]
