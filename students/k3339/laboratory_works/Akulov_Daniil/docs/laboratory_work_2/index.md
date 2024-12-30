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


# Запустить локально

## Установить зависимости

```bash
pip install django, psycopg2-binary
```

## Запустить сервер

```bash
python manage.py runserver
```