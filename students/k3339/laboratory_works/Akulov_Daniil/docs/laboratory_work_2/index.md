## Лабораторная работа 2: Список отелей

### Задание

Реализовать сайт используя фреймворк Django 3 и СУБД PostgreSQL *, в соответствии с вариантом задания лабораторной
работы. Вариант: 1 - Список отелей.

Таблицы в базе данных:

- Пользователь
- Отель
- Комната
- Бронирование
- Отзыв

Код схем базы данных:

```python
class Hotel(models.Model):
    name = models.CharField(max_length=144, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hotels")
    address = models.CharField(max_length=144)
    description = models.CharField(max_length=400)

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    number = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.PositiveIntegerField()
    room_type = models.CharField(max_length=25)
    capacity = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def is_finished(self):
        return timezone.now() > self.check_out

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reviews")
    text = models.CharField(max_length=400)
    rating = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(10)])
```

Реализован следующий функционал:

- Регистрация новых пользователей.
- Просмотр и резервирование номеров. Пользователь должен иметь
  возможность редактирования и удаления своих резервирований.
- Написание отзывов к номерам. При добавлении комментариев, должны
  сохраняться период проживания, текст комментария, рейтинг (1-10),
  информация о комментаторе.
- Администратор должен иметь возможность заселить пользователя в отель и
  выселить из отеля средствами Django-admin.
- В клиентской части должна формироваться таблица, отображающая
  постояльцев отеля за последний месяц.

Эндпоинты:
```python
urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path("logout/", LogoutView.as_view(next_page='login'), name="logout"),
    path('hotels/', views.hotels, name='hotels'),
    path('hotels/create', views.hotel_create, name='hotel-create'),
    path('hotels/update/<int:hotel_id>', views.HotelUpdateView.as_view(), name='hotel-update'),
    path('hotels/delete/<int:hotel_id>', views.HotelDeleteView.as_view(), name='hotel-delete'),
    path('<int:hotel_id>/rooms/', views.hotel_rooms, name='hotel-rooms'),
    path('<int:hotel_id>/rooms/create', views.room_create, name='room-create'),
    path('rooms/update/<int:room_id>', views.RoomUpdateView.as_view(), name='room-update'),
    path('rooms/delete/<int:room_id>', views.RoomDeleteView.as_view(), name='room-delete'),
    path('rooms/', views.rooms, name='rooms'),
    path('bookings/', views.bookings, name='bookings'),
    path('<int:hotel_id>/bookings/', views.hotel_bookings, name='hotel-bookings'),
    path('<int:hotel_id>/bookings/admin-create', views.booking_admin_create, name='booking-admin-create'),
    path('<int:room_id>/bookings/create', views.booking_create, name='booking-create'),
    path('bookings/update/<int:booking_id>', views.BookingUpdateView.as_view(), name='booking-update'),
    path('bookings/delete/<int:booking_id>', views.BookingDeleteView.as_view(), name='booking-delete'),
    path('users/last-month', views.users_last_month, name='users-last-month'),
    path('reviews/<int:room_id>', views.reviews, name='reviews'),
    path('reviews/<int:room_id>/create', views.review_create, name='review-create'),
]
```

### Запустить локально

#### Установить зависимости

```bash
pip install django, psycopg2-binary
```

#### Запустить сервер

```bash
python manage.py runserver
```