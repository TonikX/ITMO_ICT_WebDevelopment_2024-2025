# Flight Booking System Documentation

## Описание задания

**Цель работы**: Реализация сайта с использованием фреймворка Django 3 и СУБД PostgreSQL, предназначенного для отображения и управления данными о авиаперелетах.

**Функциональные требования**:

- Регистрация и авторизация пользователей.
- Просмотр и резервирование мест на рейсах.
- Управление резервированием: возможность редактирования и удаления пользователем своих резервирований.
- Администрирование через Django Admin:
- - Регистрация пассажиров на рейсы. 
- - Внесение данных о номерах билетов.
- Отображение в клиентской части списка всех пассажиров рейса.
- Добавление и просмотр отзывов к рейсам с сохранением даты рейса, текста комментария, рейтинга (1-10) и информации о комментаторе.

## Реализация

### Модели (models.py)

Модели определяют структуру базы данных для проекта.

1. **Flight**
```python
   class Flight(models.Model):
    number = models.CharField(max_length=10)
    airline = models.CharField(max_length=50)
    departure = models.CharField(max_length=50)
    arrival = models.CharField(max_length=50)
    flight_type = models.CharField(max_length=10, choices=[('departure', 'Departure'), ('arrival', 'Arrival')])
    gate = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.number} - {self.airline}"
  ```
**Описание**: Хранит данные о рейсе: номер рейса, авиакомпания, пункты отправления и прибытия, тип рейса, номер гейта.

2. **Reservation**
```python
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)

    def __str__(self):
        return f"Reservation: {self.user.username} - {self.flight.number} ({self.seat_number})"
```
**Описание**: Связывает пользователей с рейсами и позволяет хранить информацию о забронированных местах.

3. **Review**
```python
class Review(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"Review by {self.user.username} - {self.flight.number} ({self.rating}/10)"
```
**Описание**: Хранит отзывы пользователей о рейсах, включая текст, дату, рейтинг и автора.

### Формы (forms.py)
Формы используются для ввода данных пользователем через интерфейс.

1. **ReservationForm**
```python
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['seat_number']
```
Описание: Форма для бронирования мест на рейсах.

2. **ReviewForm**
```python
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['date', 'text', 'rating']
```
Описание: Форма для добавления отзывов к рейсам.

### Представления (views.py)

Логика обработки запросов и отображения страниц.

1. **flight_list**
```python
@login_required
def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'flights/flight_list.html', {'flights': flights})
```
**Описание**: Отображает список всех рейсов.

2. **reserve_seat**
```python
@login_required
def reserve_seat(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.flight = flight
            reservation.save()
            return redirect('flight_list')
    else:
        form = ReservationForm()
    return render(request, 'flights/reserve_seat.html', {'form': form, 'flight': flight})
```
**Описание**: Реализует функционал бронирования мест на рейсах.

3. **flight_reviews**
```python
@login_required
def flight_reviews(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    reviews = Review.objects.filter(flight=flight)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.flight = flight
            review.save()
            return redirect('flight_reviews', flight_id=flight_id)
    else:
        form = ReviewForm()
    return render(request, 'flights/flight_reviews.html', {'flight': flight, 'reviews': reviews, 'form': form})
```
**Описание**: Отображает отзывы о рейсе и позволяет добавлять новые.

4. **register**
```python
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('flight_list')
    else:
        form = UserCreationForm()
    return render(request, 'flights/register.html', {'form': form})
```
**Описание**: Обеспечивает регистрацию новых пользователей.
   
5. **login_view и logout_view**
```python
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('flight_list')
    else:
        form = AuthenticationForm()
    return render(request, 'flights/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
```
**Описание**: Обеспечивают вход и выход пользователей из системы.

6. **add_review**
```python
@login_required
def add_review(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.flight = flight
            review.save()
            return redirect('flight_reviews', flight_id=flight_id)
    else:
        form = ReviewForm()
    return render(request, 'flights/add_review.html', {'form': form, 'flight': flight})
```
**Описание**: Реализует добавление отзывов о рейсах.

### Django Admin (admin.py)

Встроенный инструмент фреймворка Django, предназначенный для управления данными в приложении через удобный веб-интерфейс.
Предназначен для:
- Управление данными без необходимости писать код;
- Разграничение доступа;
- Кастомизация интерфейса (настройка отображения данных, добавление фильтров, поиск, группировка и прочее для удобства администраторов).

1. **FlightAdmin**
```python
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('number', 'airline', 'departure', 'arrival', 'flight_type', 'gate')
```
**Описание**: Управление данными о рейсах.

2. **ReservationAdmin**
```python
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'flight', 'seat_number')
   ```
**Описание**: Управление бронированиями.

3. **ReviewAdmin**
```python
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('flight', 'user', 'date', 'rating')
   ```
**Описание**: Управление отзывами.

### **URLs (urls.py)**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.flight_list, name='flight_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reserve/<int:flight_id>/', views.reserve_seat, name='reserve_seat'),
    path('reviews/<int:flight_id>/', views.flight_reviews, name='flight_reviews'),
    path('add_review/<int:flight_id>/', views.add_review, name='add_review'),
]
```

**Описание маршрутов**:

- ```/``` - Отображает список доступных рейсов (функция flight_list).
- ```/register/```- Регистрация нового пользователя (функция register).
- ``` /login/```  - Вход пользователя в систему (функция login_view).
- ``` /logout/```  - Выход пользователя из системы (функция logout_view).
- ``` /reserve/<int:flight_id>/```  - Бронирование мест на рейсе с ID flight_id (функция reserve_seat).
- ``` /reviews/<int:flight_id>/```  - Отображает отзывы о рейсе с ID flight_id (функция flight_reviews).
- ``` /add_review/<int:flight_id>/```  - Добавление отзыва о рейсе с ID flight_id (функция add_review).

### HTML-страницы
1. **add_review.html**
**Описание**: Страница для добавления нового отзыва о рейсе.
```python
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Review</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="card shadow">
            <div class="card-header bg-primary text-white">
                <h3>Add Review for Flight {{ flight.number }}</h3>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-success w-100">Submit Review</button>
                </form>
                <a href="{% url 'flight_reviews' flight.id %}" class="btn btn-secondary mt-3 w-100">Back to Reviews</a>
            </div>
        </div>
    </div>
</body>
</html>
```


2.**flight_list.html**
**Описание**: Отображает список доступных рейсов с возможностью бронирования и просмотра отзывов.
```python
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flight List</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center mb-4">Available Flights</h1>
        <div class="d-flex justify-content-between mb-3">
            {% if user.is_authenticated %}
                <a href="{% url 'logout' %}" class="btn btn-danger">Logout</a>
            {% else %}
                <a href="{% url 'login' %}" class="btn btn-primary">Login</a>
                <a href="{% url 'register' %}" class="btn btn-secondary">Register</a>
            {% endif %}
        </div>
        <table class="table table-bordered table-hover">
            <thead class="table-dark">
                <tr>
                    <th>Number</th>
                    <th>Airline</th>
                    <th>Departure</th>
                    <th>Arrival</th>
                    <th>Type</th>
                    <th>Gate</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for flight in flights %}
                <tr>
                    <td>{{ flight.number }}</td>
                    <td>{{ flight.airline }}</td>
                    <td>{{ flight.departure }}</td>
                    <td>{{ flight.arrival }}</td>
                    <td>{{ flight.flight_type }}</td>
                    <td>{{ flight.gate }}</td>
                    <td>
                        <a href="{% url 'reserve_seat' flight.id %}" class="btn btn-success btn-sm">Reserve</a>
                        <a href="{% url 'flight_reviews' flight.id %}" class="btn btn-info btn-sm">Reviews</a>
                        <a href="{% url 'add_review' flight.id %}" class="btn btn-warning btn-sm">Add Review</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>

```
   
3. **flight_reviews.html**
**Описание**: Страница для отображения отзывов о рейсе.
```python
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flight Reviews</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>Reviews for Flight {{ flight.number }}</h1>
        <a href="{% url 'add_review' flight.id %}" class="btn btn-primary mb-3">Add a Review</a>
        <div class="list-group">
            {% for review in reviews %}
                <div class="list-group-item">
                    <h5>{{ review.user.username }} - {{ review.date }}</h5>
                    <p>{{ review.text }}</p>
                    <small>Rating: {{ review.rating }}/10</small>
                </div>
            {% empty %}
                <p>No reviews yet.</p>
            {% endfor %}
        </div>
        <a href="{% url 'flight_list' %}" class="btn btn-secondary mt-3">Back to Flights</a>
    </div>
</body>
</html>
```
4. **login.html**
**Описание**: Страница для входа пользователя в систему.
```python
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="card shadow">
            <div class="card-header bg-primary text-white">
                <h3>Login</h3>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>
                <p class="text-center mt-3">
                    Don't have an account? <a href="{% url 'register' %}">Register</a>
                </p>
            </div>
        </div>
    </div>
</body>
</html>
```

5. **register.html**
**Описание**: Страница для регистрации нового пользователя.
```python
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="card shadow">
            <div class="card-header bg-primary text-white">
                <h3>Register</h3>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-success w-100">Register</button>
                </form>
                <p class="text-center mt-3">
                    Already have an account? <a href="{% url 'login' %}">Login</a>
                </p>
            </div>
        </div>
    </div>
</body>
</html>
```

6. **reserve_seat.html**
**Описание**: Страница для бронирования места на рейсе.
```python
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reserve Seat for {{ flight.number }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center">Reserve a Seat for Flight {{ flight.number }}</h1>
        <div class="card mt-4">
            <div class="card-body">
                <h5 class="card-title">Flight Details</h5>
                <p><strong>Airline:</strong> {{ flight.airline }}</p>
                <p><strong>Departure:</strong> {{ flight.departure }}</p>
                <p><strong>Arrival:</strong> {{ flight.arrival }}</p>
                <p><strong>Type:</strong> {{ flight.flight_type }}</p>
                <p><strong>Gate:</strong> {{ flight.gate }}</p>
            </div>
        </div>
        <div class="mt-4">
            <h5 class="mb-3">Reserve Your Seat</h5>
            <form method="post">
                {% csrf_token %}
                <div class="mb-3">
                    {{ form.as_p }}
                </div>
                <button type="submit" class="btn btn-primary">Reserve</button>
                <a href="{% url 'flight_list' %}" class="btn btn-secondary">Cancel</a>
            </form>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```
