# Вариант № 4: Список туров туристической фирмы

`Задание`: Хранится информация о названии тура, турагенстве, описании тура, периоде
проведения тура, условиях оплаты.

Необходимо реализовать следующий функционал:

- Регистрация новых пользователей.
- Просмотр и резервирование туров. Пользователь должен иметь возможность редактирования и удаления своих резервирований.
- Написание отзывов к турам. При добавлении комментариев, должны сохраняться даты тура, текст комментария, рейтинг (1-10), информация о комментаторе.
- Администратор должен иметь возможность подтвердить резервирование тура средствами Django-admin.
- В клиентской части должна формироваться таблица, отображающая все проданные туры по странам.

### 1. Создание проекта и настройка:

Сначала создаем виртуальное окружение для изоляции зависимостей проекта. Открываем терминал и выполняем:

```bash
python -m venv venv
source venv/bin/activate
pip install django

django-admin startproject tourfirm

python manage.py startapp tour_app
```

Открываем файл tourfirm/settings.py и добавляем наше приложение в список INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tour_app',  # добавляем наше приложение
]
```

### 2. Создание моделей в файле `models.py`

Файл `models.py` определяет структуру базы данных. Каждый класс модели соответствует таблице в БД, а атрибуты класса - столбцам таблицы.

Объяснение реализованных моделей:

- `Tour`: Модель для хранения информации о турах (название, агентство, описание, страна, даты, цена)
- `Reservation`: Модель для бронирований туров пользователями с различными статусами
- `Review`: Модель для отзывов о турах с рейтингом от 1 до 10

#### `Модель Tour (Тур)`

```python
class Tour(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название тура")
    agency = models.CharField(max_length=200, verbose_name="Турагенство")
    description = models.TextField(verbose_name="Описание тура")
    country = models.CharField(max_length=100, verbose_name="Страна")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    payment_conditions = models.TextField(verbose_name="Условия оплаты")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"
        ordering = ['start_date']

    def __str__(self):
        return f"{self.title} - {self.agency}"
```

Атрибуты:

- `title` - название тура (CharField, макс. 200 символов)
- `agency` - название турагенства (CharField)
- `description` - подробное описание тура (TextField для длинного текста)
- `country` - страна назначения (CharField)
- `start_date`, `end_date` - даты начала и окончания тура (DateField)
- `payment_conditions` - условия оплаты (TextField)
- `price` - цена тура (DecimalField для точных денежных расчетов)
- `created_at` - автоматическая дата создания записи (auto_now_add=True)

`Meta` класс:

- `verbose_name` - человекочитаемое имя в единственном числе для админки
- `verbose_name_plural` - имя во множественном числе
- `ordering` - автоматическая сортировка по дате начала тура

Метод `str`: Возвращает строковое представление объекта для удобного отображения в админке и шаблонах.

#### `Модель Reservation (Бронирование)`

```python
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтвержден'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="Тур")
    reservation_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата резервирования")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    notes = models.TextField(blank=True, verbose_name="Примечания")

    class Meta:
        verbose_name = "Резервирование"
        verbose_name_plural = "Резервирования"
        unique_together = ['user', 'tour']

    def __str__(self):
        return f"{self.user.username} - {self.tour.title}"
```

- `STATUS_CHOICES` - список возможных статусов бронирования с человекочитаемыми названиями
- `user` - связь с моделью User (ForeignKey), каскадное удаление
- `tour` - связь с моделью Tour (ForeignKey)
- `reservation_date` - автоматическая дата бронирования
- `status` - статус брони с выбором из предопределенных значений
- `notes` - примечания пользователя (может быть пустым)
- `unique_together`: Гарантирует, что один пользователь не может забронировать один тур multiple раз.

#### `Модель Review (Отзыв)`

```python
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="Тур")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Рейтинг"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    tour_start_date = models.DateField(verbose_name="Дата начала тура")
    tour_end_date = models.DateField(verbose_name="Дата окончания тура")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ['user', 'tour']

    def __str__(self):
        return f"{self.user.username} - {self.tour.title} - {self.rating}/10"
```

- `user`, `tour` - связи с пользователем и туром
- `text` - текст отзыва
- `rating` - рейтинг от 1 до 10 с валидаторами минимального и максимального значения
- `created_at` - дата создания отзыва
- `tour_start_date`, `tour_end_date` - фактические даты поездки пользователя

ordering: Сортировка от новых к старым отзывам

Создаем файлы миграций на основе наших моделей и применяем их к базе данных:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Настройка админ-панели в `admin.py`

Файл admin.py настраивает отображение и поведение моделей в административной панели Django.

Регистрируем наши модели в административной панели Django для удобного управления данными:

#### `Админ-класс для Tour`

```python
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['title', 'agency', 'country', 'start_date', 'end_date', 'price']
    list_filter = ['agency', 'country', 'start_date']
    search_fields = ['title', 'description']
```

- `list_display` - какие поля показывать в списке объектов
- `list_filter` - по каким полям можно фильтровать список
- `search_fields` - по каким полям осуществляется поиск

#### `Админ-класс для Reservation`

```python
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour', 'reservation_date', 'status']
    list_filter = ['status', 'reservation_date']
    search_fields = ['user__username', 'tour__title']
    list_editable = ['status']
    actions = ['confirm_reservations']

    def confirm_reservations(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, f'{queryset.count()} резервирований подтверждено')
    confirm_reservations.short_description = "Подтвердить выбранные резервирования"
```

- `list_editable` - позволяет редактировать статус прямо из списка
- `actions` - кастомные действия для массового применения
- `confirm_reservations` - метод для массового подтверждения бронирований

#### `Админ-класс для Review`

```python
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'tour__title', 'text']
```

Позволяет администраторам просматривать и управлять отзывами, фильтровать по рейтингу и дате.

### 3. Создаем представления в `views.py` для обработки запросов и отображения страниц:

Файл `views.py` содержит всю бизнес-логику приложения - обработку запросов, работу с данными, рендеринг шаблонов.

#### `Функция home - Главная страница`

```python
def home(request):
    tours = Tour.objects.all()
    return render(request, 'home.html', {'tours': tours})
```

Получает все туры из БД и передает их в шаблон для отображения.

#### `Функция register - Регистрация пользователя`

```python
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
```

Логика работы:

- Если POST-запрос - обрабатываем данные формы
- Если форма валидна - сохраняем пользователя, логиним его и показываем сообщение
- Если GET-запрос - показываем пустую форму

#### `Функция custom_logout - Выход из системы`

```python
@csrf_protect
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы.')
        return redirect('login')
    else:
        # Если кто-то попытается выйти через GET, перенаправляем на главную
        return redirect('home')
```

- Использует @csrf_protect для защиты от CSRF-атак
- Принимает только POST-запросы для безопасности
- Показывает сообщение об успешном выходе

#### `Функция tour_detail - Детали тура`

```python
@login_required
def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    user_reservation = None
    user_review = None

    if request.user.is_authenticated:
        user_reservation = Reservation.objects.filter(user=request.user, tour=tour).first()
        user_review = Review.objects.filter(user=request.user, tour=tour).first()

    reviews = Review.objects.filter(tour=tour).exclude(user=request.user)

    if request.method == 'POST':
        if 'reserve' in request.POST:
            reservation_form = ReservationForm(request.POST)
            if reservation_form.is_valid() and not user_reservation:
                reservation = reservation_form.save(commit=False)
                reservation.user = request.user
                reservation.tour = tour
                reservation.save()
                messages.success(request, 'Тур успешно забронирован!')
                return redirect('tour_detail', tour_id=tour_id)

        elif 'review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                if user_review:
                    review_form = ReviewForm(request.POST, instance=user_review)
                    review = review_form.save()
                    messages.success(request, 'Отзыв обновлен!')
                else:
                    review = review_form.save(commit=False)
                    review.user = request.user
                    review.tour = tour
                    review.save()
                    messages.success(request, 'Отзыв добавлен!')
                return redirect('tour_detail', tour_id=tour_id)
    else:
        reservation_form = ReservationForm(instance=user_reservation)
        review_form = ReviewForm(instance=user_review)

    return render(request, 'tour_detail.html', {
        'tour': tour,
        'reservation_form': reservation_form,
        'review_form': review_form,
        'user_reservation': user_reservation,
        'user_review': user_review,
        'reviews': reviews,
    })
```

Логика обработки:

1. Получение данных:

- Тур по ID (с обработкой 404 ошибки)
- Бронирование и отзыв текущего пользователя для этого тура
- Все отзывы о туре

2. Обработка POST-запросов:

- Разделение на бронирование и отзыв по имени кнопки
- Для бронирования: проверка, что пользователь еще не бронировал этот тур
- Для отзыва: обновление существующего или создание нового

3. Использование commit=False: Позволяет установить дополнительные поля перед сохранением
4. Перенаправление: После успешных операций - редирект на эту же страницу для предотвращения повторной отправки формы

#### `Функция my_reservations - Мои бронирования`

```python
@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'my_reservations.html', {'reservations': reservations})
```

Показывает бронирования текущего пользователя.

#### `Функции edit_reservation и delete_reservation`

```python
@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Резервирование обновлено!')
            return redirect('my_reservations')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'edit_reservation.html', {'form': form, 'reservation': reservation})
```

```python
@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Резервирование удалено!')
        return redirect('my_reservations')

    return render(request, 'delete_reservation.html', {'reservation': reservation})
```

`get_object_or_404(Reservation, id=reservation_id, user=request.user)` гарантирует, что пользователь может редактировать/удалять только свои бронирования.

#### `Функция sold_tours_by_country - Статистика`

```python
def sold_tours_by_country(request):
    # Туры с подтвержденными резервированиями
    sold_tours = Tour.objects.filter(
        reservation__status='confirmed'
    ).annotate(
        reservations_count=Count('reservation'),
        total_sold=Sum('reservation__tour__price')
    ).order_by('country')

    return render(request, 'sold_tours.html', {'sold_tours': sold_tours})
```

Запросы к БД:

- `filter(reservation__status='confirmed')` - только туры с подтвержденными бронированиями
- `annotate()` - добавляет вычисляемые поля:
  - `reservations_count` - количество бронирований
  - `total_sold` - общая сумма продаж
  - `order_by('country')` - сортировка по странам

4. Создаем файл `urls.py` для маршрутизации внутри приложения:

```python
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from tour_app import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('reservation/edit/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('reservation/delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('sold-tours/', views.sold_tours_by_country, name='sold_tours'),
]
```

### 3. В `forms.py` создадим формы регистрации и логина

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Review

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating', 'tour_start_date', 'tour_end_date']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'form-control'}),
            'tour_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tour_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
```
