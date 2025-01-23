# Маршруты

```python
from django.urls import path
from . import views

urlpatterns = [
    # Аутентификация
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),

    # Концерты
    path('concerts/', views.concert_list, name='concert-list'),
    path('concerts/', views.create_concert, name='create_concert'),
    path('concerts/<int:pk>/', views.concert_detail, name='concert-detail'),
    path('concerts/<int:pk>/', views.update_concert, name='update_concert'),
    path('concerts/<int:pk>/delete/', views.delete_concert, name='delete_concert'),

    # Оборудование для концертов
    path('concerts/equipment/', views.add_equipment_to_concert, name='add_equipment_to_concert'),
    path('concerts/<int:concert_id>/equipment/', views.get_equipment_for_concert, name='get_equipment_for_concert'),
    path('concerts/equipment/<int:pk>/remove/', views.remove_equipment_from_concert, name='remove_equipment_from_concert'),
    path('concerts/equipment/<int:pk>/update/', views.update_equipment_for_concert, name='update_equipment_for_concert'),

    # Билеты
    path('tickets/', views.ticket_list_create, name='ticket-list-create'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket-detail'),

    # Заказы
    path('orders/', views.order_list_create, name='order-list-create'),
    path('orders/<int:pk>/', views.get_order, name='get_order'),
    path('orders/<int:pk>/confirm/', views.confirm_order, name='confirm-order'),

    # Организаторы
    path("organizer/assign/<int:pk>/", views.assign_concert, name="assign_concert"),
    path("organizer/concerts/", views.get_organizer_concerts, name="organizer-concerts"),
]
```

## Аутентификация
- **auth/register/** – Регистрация пользователя.
- **auth/login/** – Вход пользователя.
- **auth/logout/** – Выход пользователя.

## Концерты
- **concerts/** – Получение списка концертов.
- **concerts/** – Создание нового концерта.
- **concerts/<int:pk>/** – Просмотр деталей конкретного концерта.
- **concerts/<int:pk>/** – Обновление данных концерта.
- **concerts/<int:pk>/delete/** – Удаление концерта.

## Оборудование для концертов
- **concerts/equipment/** – Добавление оборудования к концерту.
- **concerts/<int:concert_id>/equipment/** – Получение списка оборудования для конкретного концерта.
- **concerts/equipment/<int:pk>/remove/** – Удаление оборудования из концерта.
- **concerts/equipment/<int:pk>/update/** – Обновление данных об оборудовании для концерта.

## Билеты
- **tickets/** – Получение списка билетов / Создание нового билета.
- **tickets/<int:pk>/** – Просмотр деталей конкретного билета.

## Заказы
- **orders/** – Получение списка заказов / Создание нового заказа.
- **orders/<int:pk>/** – Просмотр деталей заказа.
- **orders/<int:pk>/confirm/** – Подтверждение заказа.

## Организаторы
- **organizer/assign/<int:pk>/** – Назначение организатора на концерт.
- **organizer/concerts/** – Получение списка концертов, закрепленных за организатором.

