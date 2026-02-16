# Отчёт по лабораторным работам  
## Дисциплина: Основы Web-программирования

---

## 📚 Содержание

- [Лабораторная работа №2 — РЕАЛИЗАЦИЯ ПРОСТОГО САЙТА СРЕДСТВАМИ DJANGO](#лабораторная-работа-2)
- [Лабораторная работа №3 — РЕАЛИЗАЦИЯ СЕРВЕРНОЙ ЧАСТИ ПРИЛОЖЕНИЯ СРЕДСТВАМИ DJANGO И DJANGORESTFRAMEWORK](#лабораторная-работа-3)

---


# Лабораторная работа 2
## Разработка веб-приложения средствами Django
<a name="лабораторная-работа-2"></a>


**Вариант №4 — “Список туров туристической фирмы”**

---

## Цель работы
овладеть практическими навыками и умениями реализации web-сервисов
средствами Django 2.2  

Создать сайт туристической фирмы, позволяющий пользователям:

1. регистрироваться и авторизовываться,
2. просматривать туры,
3. бронировать туры и управлять своими бронями,
4. оставлять отзывы с рейтингом (1–10),
5. просматривать статистику проданных туров по странам.
#  Cтруктура проекта

```markdown
tour_agency/
├── manage.py
├── tour_agency/
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
└── tours/
├── admin.py
├── apps.py
├── models.py
├── views.py
├── urls.py
├── templates/
│ └── tours/
│ ├── base.html
│ ├── tour_list.html
│ ├── my_reservations.html
│ ├── add_review.html
│ ├── tour_detail.html
│ └── sold_tours.html
└── migrations/
└── 0001_initial.py
```
### 1. Создание и настройка проекта
1. Установлено виртуальное окружение и необходимые пакеты:
   ```bash
   pip install django psycopg2-binary bootstrap5 mkdocs
   ```
2. Создан проект:

```bash
django-admin startproject tour_agency
python manage.py startapp tours
```
Добавлено приложение tours в INSTALLED_APPS и настроено подключение к PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tour_db',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
### Вывод:
Базовая структура Django-проекта создана, связь с PostgreSQL установлена.

### 2. Моделирование данных
Определены три модели:
```python
class Tour(models.Model):
    name = models.CharField(max_length=100)
    agency = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='')
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    payment_terms = models.TextField()

    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    reserved_on = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} → {self.tour.name}"


class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(default=5)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tour.name} ({self.rating}/10)"
```        

### Вывод:
Созданы взаимосвязанные модели, реализующие основные сущности предметной области:
тур, бронирование и отзыв. Связи построены по принципу “один-ко-многим” через ForeignKey.

### 3. Настройка маршрутов (urls.py)

Созданы пути для всех функций приложения:
```python
urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tours/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('reserve/<int:tour_id>/', views.reserve_tour, name='reserve_tour'),
    path('my_reservations/', views.my_reservations, name='my_reservations'),
    path('delete_reservation/<int:res_id>/', views.delete_reservation, name='delete_reservation'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('review/<int:tour_id>/', views.add_review, name='add_review'),
    path('sold_tours/', views.sold_tours, name='sold_tours'),
]
```
### Вывод:
Маршрутизация реализована в соответствии с архитектурой MVC — каждая страница приложения обрабатывается отдельным view-функцией.

### 4. Реализация представлений (views.py)

**tour_list** — отображает все туры.

**register, login, logout** — регистрация и аутентификация пользователей.

**reserve_tour, my_reservations, delete_reservation** — операции с бронированиями.

**add_review, tour_detail** — добавление и просмотр отзывов.

**sold_tours** — аналитика продаж по странам.

### 5. Шаблоны и дизайн

Для клиентской части использован Bootstrap 5.
Создана базовая структура шаблонов:
```markdown
base.html – общая навигация
tour_list.html – список туров
my_reservations.html – личные брони
tour_detail.html – описание тура + отзывы
add_review.html – форма добавления отзыва
sold_tours.html – таблица проданных туров
```
### 6. Админ-панель Django

Добавлены модели Tour, Reservation, Review.

Администратор подтверждает бронирования через флаг Confirmed.
![img_4.png](img_4.png)

### Вывод:
Админ-интерфейс полностью функционален и позволяет управлять всеми данными без прямого доступа к БД.

### 7. Реализация аналитической таблицы

Создан метод sold_tours:
```python
def sold_tours(request):
    data = (
        Reservation.objects.filter(confirmed=True)
        .values('tour__country', 'tour__name', 'tour__agency')
        .annotate(sold_count=Count('id'))
        .order_by('tour__country')
    )
    return render(request, 'tours/sold_tours.html', {'data': data})
```
### Вывод:
Собирается статистика по странам и турам.
Подтверждённые бронирования отображаются в виде таблицы с количеством продаж.

### 8. Тестирование работы сайта
| Проверяемый функционал | Результат                       |
| ---------------------- | ------------------------------- |
| Регистрация и вход     |  Успешно                        |
| Просмотр туров         |  Отображаются все туры          |
| Бронирование           |  Создаётся запись в БД          |
| Подтверждение админом  |  Статус меняется на “Подтверждено” |
| Удаление брони         |  Успешно                        |
| Добавление отзывов     |  Отображаются с именем и рейтингом |
| Таблица продаж         |  Работает и сортируется по странам |

### Примеры экранов интерфейса

Главная страница (список туров):
![img.png](img.png)

Личные брони:
![img_1.png](img_1.png)

Описание тура с отзывами:
![img_2.png](img_2.png)

Проданные туры по странам:
![img_3.png](img_3.png)

### Общий вывод

В результате выполнения лабораторной работы было создано полноценное веб-приложение туристической фирмы на фреймворке Django с использованием базы данных PostgreSQL.
Система реализует все основные функции, указанные в задании:

- регистрация и авторизация пользователей;
- просмотр и бронирование туров;
- редактирование и удаление собственных бронирований;
- добавление отзывов и выставление рейтингов;
- подтверждение бронирований администратором через встроенную панель Django-admin;
- формирование таблицы проданных туров по странам.

В ходе работы были закреплены практические навыки:

- проектирования моделей данных и связей между ними;
- использования ORM Django для взаимодействия с базой данных;
- построения маршрутов и шаблонов;
- организации клиентского интерфейса с помощью Bootstrap 5;
- работы с админ-панелью и системой аутентификации пользователей.

Итоговый продукт имеет понятный интерфейс, чёткую структуру и легко расширяется.


# Лабораторная работа 3
## Реализация серверной части средствами Django REST Framework
<a name="лабораторная-работа-3"></a>

## Цель работы

Овладеть практическими навыками разработки серверной части
web-приложения с использованием:

- Django
- Django REST Framework (DRF)
- Djoser
- Swagger (drf-spectacular)

## Описание работы

В рамках лабораторной работы была реализована серверная часть
информационной системы администратора гостиницы.

Разработанная серверная часть обеспечивает:

- хранение данных о номерах гостиницы;
- хранение сведений о клиентах;
- регистрацию проживания клиентов;
- хранение данных о сотрудниках;
- формирование расписания уборки;
- выполнение аналитических запросов;
- формирование отчётов.

Серверная часть разработана средствами Django REST Framework.

## Модель базы данных

Для реализации системы была разработана модель базы данных
с использованием Django ORM.

В системе используются следующие сущности:

- Room — номер гостиницы;
- Guest — клиент гостиницы;
- Stay — проживание клиента;
- Staff — сотрудник гостиницы;
- CleaningSchedule — расписание уборки.

Связи между сущностями реализованы средствами ForeignKey.

### Пример реализации модели
```python
class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('triple', 'Triple'),
    ]

    number = models.IntegerField(unique=True)
    floor = models.IntegerField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Room {self.number}"


class Guest(models.Model):
    passport_number = models.CharField(max_length=50, unique=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    city_from = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Stay(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    check_in = models.DateField()
    check_out = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.guest} -> {self.room}"


class Staff(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class CleaningSchedule(models.Model):
    WEEKDAYS = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAYS)
    floor = models.IntegerField()

    def __str__(self):
        return f"{self.staff} - {self.get_weekday_display()} - floor {self.floor}"
```
# Реализация REST API
REST API реализовано средствами Django REST Framework.

Для взаимодействия с данными были разработаны:
- сериализаторы;
- ViewSet-классы;
- маршруты.

Реализованы стандартные CRUD-операции:
- получение данных (GET);
- создание записей (POST);
- изменение данных (PUT / PATCH);
- удаление записей (DELETE).

### Пример реализации сериализатора
```python 
from rest_framework import serializers
from .models import Room, Guest, Stay, Staff, CleaningSchedule

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'

class StaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stay
        fields = '__all__'

    def validate(self, data):
        room = data.get('room')
        check_in = data.get('check_in')
        check_out = data.get('check_out')

        if check_in >= check_out:
            raise serializers.ValidationError("check_out must be after check_in")

        overlapping_stays = Stay.objects.filter(
            room=room
        ).filter(
            Q(check_in__lt=check_out) & Q(check_out__gt=check_in)
        )

        if self.instance:
            overlapping_stays = overlapping_stays.exclude(id=self.instance.id)

        if overlapping_stays.exists():
            raise serializers.ValidationError("Номер уже занят в этот период 😎")

        return data

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class CleaningScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleaningSchedule
        fields = '__all__'
```
### Пример реализации ViewSet
```python 
class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name='city', type=str, required=True),
        ]
    )
    @action(detail=False, methods=['get'])
    def by_city(self, request):
        city = request.query_params.get('city')
        count = Guest.objects.filter(city_from=city).count()

        return Response({
            "city": city,
            "count": count
        })
```
# Реализация бизнес-логики
В системе была реализована дополнительная логика обработки данных.

В частности:
- получение списка свободных номеров;
- получение количества клиентов из заданного города;
- получение клиентов, проживавших в номере за указанный период;
- определение сотрудника, выполняющего уборку номера;
- формирование квартального отчёта;
- проверка пересечения периодов проживания клиентов.
- Проверка пересечения дат проживания предотвращает возможность двойного бронирования номера.

### Пример реализации бизнес-логики
```python
@extend_schema(
        parameters=[
            OpenApiParameter(name='guest', type=int, required=True),
            OpenApiParameter(name='weekday', type=int, required=True),
        ]
    )
    @action(detail=False, methods=['get'])
    def cleaner(self, request):
        guest_id = request.query_params.get('guest')
        weekday = request.query_params.get('weekday')

        if not guest_id or not weekday:
            return Response({"error": "guest and weekday are required"}, status=400)

        try:
            weekday = int(weekday)
        except ValueError:
            return Response({"error": "weekday must be int"}, status=400)

        stay = Stay.objects.filter(
            guest_id=guest_id,
            check_out__isnull=True
        ).select_related('room', 'guest').first()

        if not stay:
            return Response({"error": "Guest not staying now"}, status=404)

        floor = stay.room.floor

        schedules = CleaningSchedule.objects.filter(
            floor=floor,
            weekday=weekday
        ).select_related('staff')

        if not schedules.exists():
            return Response({"message": "No cleaning scheduled for this floor/day"}, status=200)

        return Response({
            "guest_id": stay.guest_id,
            "room_number": stay.room.number,
            "floor": floor,
            "weekday": weekday,
            "cleaners": [
                f"{s.staff.last_name} {s.staff.first_name}" for s in schedules
            ]
        })
```
# Документация и тестирование API
Для документирования и тестирования REST API использовался Swagger UI, реализованный через библиотеку drf-spectacular.

Swagger UI позволяет:
- просматривать доступные endpoint-ы;
- выполнять тестовые запросы;
- передавать параметры;
- анализировать ответы сервера.

# Авторизация
В системе реализована токенная авторизация средствами Djoser.

Используемые endpoints:
- POST /auth/token/login/ — получение токена;
- POST /auth/token/logout/ — завершение сессии;
- GET /auth/users/me/ — получение информации о текущем пользователе.
- Авторизация реализована на основе TokenAuthentication.

# Результаты работы

В результате выполнения лабораторной работы была разработана
серверная часть информационной системы гостиницы.

Реализованы:
- ORM-модель базы данных;
- REST API;
- бизнес-логика;
- аналитические запросы;
- механизм авторизации;
- документация API.

# Вывод
В ходе лабораторной работы были освоены навыки разработки
REST API средствами Django REST Framework.
Была реализована модель базы данных средствами Django ORM,
а также бизнес-логика и аналитические запросы.
Использование Swagger UI позволило упростить процесс тестирования
и документирования API.
Разработанная серверная часть системы является полностью
функциональной и соответствует требованиям задания.