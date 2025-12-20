## Практическое задание 3

Cделать “Владельца автомобиля” пользователем и расширить модель пользователя его атрибутами, так, чтобы о нем хранилась следующая информация:

- номер паспорта;
- домашний адрес;
- национальность.

Отобразить новые поля пользователя в Django Admin. Отредактировать код из предыдущих работ, так, чтобы выводилась информация о пользователях.
Реализовать интерфейс создания пользователя с новыми атрибутами.

1. Обновляем `models.py` и заменяем наш класс `CarOwner` на `User`:

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    passport_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер паспорта')
    home_address = models.TextField(blank=True, null=True, verbose_name='Домашний адрес')
    nationality = models.CharField(max_length=50, blank=True, null=True, verbose_name='Национальность')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.number})"

    def get_current_owner(self):
        """Возвращает текущего владельца автомобиля"""
        current_ownership = self.ownership_set.filter(end_date__isnull=True).first()
        return current_ownership.owner if current_ownership else None

    def get_all_owners(self):
        """Возвращает всех владельцев автомобиля (текущего и прошлых)"""
        return self.ownership_set.all().order_by('-start_date')

class CarLicense(models.Model):
    license_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')
    number = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=10)
    issue_date = models.DateField()

    def __str__(self):
        return f"ВУ {self.number} ({self.type})"

class Ownership(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')
    car = models.ForeignKey('Car', on_delete=models.CASCADE, verbose_name='Автомобиль')
    start_date = models.DateField(verbose_name='Дата начала владения')
    end_date = models.DateField(blank=True, null=True, verbose_name='Дата окончания владения')

    def __str__(self):
        return f"{self.owner} - {self.car} ({self.start_date})"

    def is_current(self):
        """Проверяет, является ли владение текущим"""
        return self.end_date is None
```

2. В `settings.py` добавляем нашу кастомную модель:

```python
AUTH_USER_MODEL = 'project_first_app.User'
```

В `forms.py` создаем новую форму ввода:

```python
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                 'passport_number', 'home_address', 'nationality', 'birth_date',
                 'password1', 'password2')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'home_address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'passport_number': 'Номер паспорта',
            'home_address': 'Домашний адрес',
            'nationality': 'Национальность',
            'birth_date': 'Дата рождения',
        }
```

В `admin.py` отображаем новые поля и обновляем в связи с заменой `CarOwner`:

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Ownership, Car, CarLicense, User

class CustomUserAdmin(UserAdmin):
    # Добавляем новые поля в форму редактирования
    fieldsets = UserAdmin.fieldsets + (
        ('Информация о владельце автомобиля', {
            'fields': ('passport_number', 'home_address', 'nationality', 'birth_date')
        }),
    )

    # Добавляем новые поля в форму создания
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Информация о владельце автомобиля', {
            'fields': ('passport_number', 'home_address', 'nationality', 'birth_date')
        }),
    )

    # Добавляем новые поля в список пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'passport_number', 'home_address', 'nationality', 'is_staff')
    list_filter = ('nationality', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'passport_number', 'nationality')

class OwnershipInline(admin.TabularInline):
    model = Ownership
    extra = 1
    fields = ['car', 'start_date', 'end_date']
    verbose_name = 'Владение автомобилем'
    verbose_name_plural = 'Владения автомобилями'

class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'number', 'color', 'owners_count']
    search_fields = ['brand', 'model', 'number']

    def owners_count(self, obj):
        return obj.ownership_set.count()
    owners_count.short_description = 'Кол-во владельцев'

class UserAdminWithCars(CustomUserAdmin):
    inlines = [OwnershipInline]

    def cars_count(self, obj):
        return obj.ownership_set.count()
    cars_count.short_description = 'Кол-во автомобилей'

    list_display = CustomUserAdmin.list_display + ('cars_count',)

# Регистрируем модели
admin.site.register(User, UserAdminWithCars)
admin.site.register(Car, CarAdmin)
admin.site.register(CarLicense)
admin.site.register(Ownership)
```

В `views.py` тоже проводим изменения в связи со сменой модели:

```python
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Car
from django.contrib.auth import get_user_model
from .forms import CarForm, CustomUserCreationForm
from django.contrib import messages


User = get_user_model()

def owners(request):
    owners = User.objects.all()
    return render(request, "owners.html", {'owners': owners})

def detail(request, owner_id):
    owner = get_object_or_404(User, pk=owner_id)
    return render(request, "owner.html", {'owner': owner})

def create_owner(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Владелец успешно добавлен!')
            return redirect('owners')
    else:
        form =  CustomUserCreationForm()

    return render(request, 'owner_form.html', {'form': form})

def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Автомобиль успешно добавлен!')
            return redirect('cars')
    else:
        form = CarForm()

    return render(request, 'car_create.html', {'form': form})

class CarListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'

class CarDetailView(DetailView):
    model = Car
    template_name = 'car.html'
    context_object_name = 'car'

class CarUpdateView(UpdateView):
    model = Car
    template_name = 'car_form.html'
    fields = ['number', 'brand', 'model', 'color']
    success_url = reverse_lazy('cars')
    pk_url_kwarg = 'car_id'

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = reverse_lazy('cars')
    pk_url_kwarg = 'car_id'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Автомобиль успешно удален')
        return super().delete(request, *args, **kwargs)
```

После этого мы снова делаем миграции и меняем html-шаблоны. Получается примерно вот так:

![alt text](<Снимок экрана 2025-10-22 в 16.21.02.png>)
![alt text](<Снимок экрана 2025-10-22 в 16.20.49.png>)
![alt text](<Снимок экрана 2025-10-22 в 16.21.13.png>)
![alt text](<Снимок экрана 2025-10-22 в 16.21.32.png>)
![alt text](<Снимок экрана 2025-10-22 в 16.21.51.png>)
![alt text](<Снимок экрана 2025-10-22 в 16.22.05.png>)
![alt text](<Снимок экрана 2025-10-22 в 16.22.15.png>)
![alt text](<Снимок экрана 2025-10-22 в 16.22.23.png>)
