from django.contrib import admin
from django.urls import path, include
from . import views as tour_views

app_name = 'tours'

app_name = 'tours'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', tour_views.register, name='register'),  # Регистрировать пользователя
    path('accounts/', include('django.contrib.auth.urls')),  # Включение путей авторизации
    path('', tour_views.tour_list, name='tour_list'),  # Список всех туров
    path('tour/<int:tour_id>/', tour_views.tour_detail, name='tour_detail'),  # Детали тура
    path('tour/<int:tour_id>/reserve/', tour_views.reserve_tour, name='reserve_tour'),  # Резервировать тур
    path('my_reservations/', tour_views.my_reservations, name='my_reservations'),  # Личные резервации
    path('reservation/delete/<int:reservation_id>/', tour_views.delete_reservation, name='delete_reservation'),  # Отменить резерв
    path('tour/<int:tour_id>/review/', tour_views.add_review, name='add_review'),  # Оставить отзыв
    path('sold_tours/', tour_views.sold_tours_by_country, name='sold_tours_by_country'),  # Статистика продаж туров по странам
]