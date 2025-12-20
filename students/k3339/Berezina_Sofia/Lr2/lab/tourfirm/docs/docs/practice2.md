## Практическое задание 2: Доработка модели данных. Реализация связи “Многие ко многим”

Правильно настроить связь между автомобилем, владением и владельцем.

1. В `admin.py`:

```python
from django.contrib import admin
from .models import Car, CarOwner, CarLicense, Ownership

# Inline для отображения владений на странице владельца
class OwnershipInline(admin.TabularInline):  # или admin.StackedInline
    model = Ownership
    extra = 1  # Количество пустых форм для добавления
    raw_id_fields = ('car',)

# Inline для отображения владений на странице автомобиля
class CarOwnershipInline(admin.TabularInline):
    model = Ownership
    extra = 1
    raw_id_fields = ('owner',)

class CarOwnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'name', 'birth_date')
    search_fields = ('surname', 'name')
    list_filter = ('birth_date',)
    inlines = [OwnershipInline]  # Добавляем inline

class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'brand', 'model', 'color')
    list_filter = ('brand', 'model')
    search_fields = ('number', 'brand', 'model')
    ordering = ('brand', 'model')
    inlines = [CarOwnershipInline]  # Добавляем inline

class CarLicenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'type', 'issue_date', 'owner')
    list_filter = ('type', 'issue_date')
    search_fields = ('number', 'owner__surname', 'owner__name')
    raw_id_fields = ('owner',)

class OwnershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'car', 'start_date', 'end_date', 'duration_days')
    list_filter = ('start_date', 'end_date')
    search_fields = ('owner__surname', 'owner__name', 'car__brand', 'car__model')
    raw_id_fields = ('owner', 'car')
    date_hierarchy = 'start_date'

    # Дополнительное вычисляемое поле
    def duration_days(self, obj):
        if obj.end_date:
            delta = obj.end_date - obj.start_date
            return delta.days
        return "Владение активно"
    duration_days.short_description = 'Дней владения'

admin.site.register(Car, CarAdmin)
admin.site.register(CarOwner, CarOwnerAdmin)
admin.site.register(CarLicense, CarLicenseAdmin)
admin.site.register(Ownership, OwnershipAdmin)
```

## Практическое задание (по задаче 2)

1. Реализовать вывод всех владельцев функционально. Добавить данные минимум от трех владельцах. Должны быть реализованы контроллер (views) и шаблоны (temlates).
2. Реализовать вывод всех автомобилей, вывод автомобиля по id, обновления на основе классов. Добавить данные минимум о трех автомобилях. Должны быть реализованы контроллер (views) и шаблоны (temlates).

### Выполнение задания

1. Добавляем в `urls.py` еще один путь:

```pyhton
    path('owners/', views.owners, name='owners'),
```

Создаем представление для вывода владельцев в `views.py`:

```python
def owners_list(request):
    owners = CarOwner.objects.all()
    return render(request, 'owners.html', {'owners': owners})
```

Создаем html-файл owners.html для вывода всех владельцев:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Владельцы автомобилей</title>
</head>
<body>
    <div class="nav-links">
        <a href="{% url 'owners' %}">Владельцы</a>
    </div>

    <h1>Список владельцев автомобилей</h1>
    
    {% if owners %}
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Фамилия</th>
                    <th>Имя</th>
                    <th>Дата рождения</th>
                </tr>
            </thead>
            <tbody>
                {% for owner in owners %}
                <tr>
                    <td>{{ owner.id }}</td>
                    <td>{{ owner.surname }}</td>
                    <td>{{ owner.name }}</td>
                    <td>{{ owner.birth_date }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>Нет данных о владельцах.</p>
    {% endif %}
</body>
</html>
```

Для автомобилей проделываем то же самое:

В `views.py` добавляем новые пути:

```python
path('cars/', views.CarListView.as_view(), name='cars'),
path('cars/<int:car_id>/update/', views.CarUpdateView.as_view(), name='car_form'),
```

В `views.py` добавляем классы для вывода всех автомобилей, просмотра каждого автомобиля по id и обновления(редактирования):

```python
class CarListView(ListView):
    model = Car
    template_name = 'project_first_app/cars_list.html'
    context_object_name = 'cars'

class CarDetailView(DetailView):
    model = Car
    template_name = 'project_first_app/car_detail.html'
    context_object_name = 'car'

class CarUpdateView(UpdateView):
    model = Car
    template_name = 'project_first_app/car_form.html'
    fields = ['number', 'brand', 'model', 'color']
    success_url = reverse_lazy('cars')
```

Создаем `cars.html` для вывода всех автомобилей:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Автомобили</title>
</head>
<body>
    <div class="nav-links">
        <a href="{% url 'owners' %}">Владельцы</a>
        <a href="{% url 'cars' %}">Автомобили</a>
    </div>

    <h1>Список автомобилей</h1>
    
    {% if cars %}
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Номер</th>
                    <th>Марка</th>
                    <th>Модель</th>
                    <th>Цвет</th>
                    <th>Действия</th>
                </tr>
            </thead>
            <tbody>
                {% for car in cars %}
                <tr>
                    <td>{{ car.id }}</td>
                    <td>{{ car.number }}</td>
                    <td>{{ car.brand }}</td>
                    <td>{{ car.model }}</td>
                    <td>{{ car.color|default:"Не указан" }}</td>
                    <td class="action-links">
                        <a href="{% url 'car' car.id %}">Просмотр</a>
                        <a href="{% url 'car_form' car.id %}">Редактировать</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>Нет данных об автомобилях.</p>
    {% endif %}
</body>
</html>
```

Создаем `car_form.html` для возможности редактирования(обновления) автомобиля:

```python
<!DOCTYPE html>
<html>
<head>
    <title>Редактирование автомобиля</title>
</head>
<body>
    <div class="nav-links">
        <a href="{% url 'owners' %}">Владельцы</a>
        <a href="{% url 'cars' %}">Автомобили</a>
    </div>

    <h1>Редактирование автомобиля</h1>
    
    <div class="form-container">
        <form method="post">
            {% csrf_token %}
            
            <div class="form-group">
                <label for="id_number">Номер:</label>
                {{ form.number }}
            </div>
            
            <div class="form-group">
                <label for="id_brand">Марка:</label>
                {{ form.brand }}
            </div>
            
            <div class="form-group">
                <label for="id_model">Модель:</label>
                {{ form.model }}
            </div>
            
            <div class="form-group">
                <label for="id_color">Цвет:</label>
                {{ form.color }}
            </div>
            
            <button type="submit">Сохранить изменения</button>
            <a href="{% url 'cars' %}" style="margin-left: 10px;">Отмена</a>
        </form>
    </div>
</body>
</html>
```

## Практическое задание (по задаче 3)

1. Реализовать форму ввода всех владельцев функционально. Добавить данные минимум о еще трех владельцах. Должны быть реализованы форма (Form), контроллер (views) и шаблоны (temlates).
2. Реализовать форму ввода, обновления и удаления всех автомобилей на основе классов. Добавить данные минимум о еще трех автомобилях. Должны быть реализованы форма (Form), контроллер (views) и шаблоны (temlates).

### Выполнение задания

Для того, чтобы реализовать ввод владельцев, нам понадобится создать файл `forms.py`:

```python
from django import forms
from .models import CarOwner

class CarOwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = ['surname', 'name', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'surname': forms.TextInput(attrs={'placeholder': 'Введите фамилию'}),
            'name': forms.TextInput(attrs={'placeholder': 'Введите имя'}),
        }
        labels = {
            'surname': 'Фамилия',
            'name': 'Имя', 
            'birth_date': 'Дата рождения',
        }
```

В `views.py` создаем представление для создания владельца:

```python
def create_owner(request):
    if request.method == 'POST':
        form = CarOwnerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Владелец успешно добавлен!')
            return redirect('owners')
    else:
        form = CarOwnerForm()
    
    return render(request, 'owner_form.html', {'form': form})
```

Создаем `owner_forn.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Добавление владельца</title>
</head>
<body>
    <div class="nav-links">
        <a href="{% url 'owners' %}">Все владельцы</a>
        <a href="{% url 'cars' %}">Все автомобили</a>
    </div>

    <h1>➕ Добавление владельца</h1>

    <div class="form-container">
        <form method="post">
            {% csrf_token %}
            
            <div class="form-group">
                <label for="id_surname">Фамилия:</label>
                {{ form.surname }}
                {% if form.surname.errors %}
                <div class="error">{{ form.surname.errors }}</div>
                {% endif %}
            </div>
            
            <div class="form-group">
                <label for="id_name">Имя:</label>
                {{ form.name }}
                {% if form.name.errors %}
                <div class="error">{{ form.name.errors }}</div>
                {% endif %}
            </div>
            
            <div class="form-group">
                <label for="id_birth_date">Дата рождения:</label>
                {{ form.birth_date }}
                {% if form.birth_date.errors %}
                <div class="error">{{ form.birth_date.errors }}</div>
                {% endif %}
            </div>

            <button type="submit" class="btn">➕ Добавить владельца</button>
            <a href="{% url 'owners' %}" class="btn-cancel">❌ Отмена</a>
        </form>
    </div>
</body>
</html>
```

Для автомобилей реализовываем создание и удаление автособиля.

В `view.py` добавляем классы для добавления и удаления автомобилей:

```python
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('cars')
    pk_url_kwarg = 'car_id'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Автомобиль успешно удален')
        return super().delete(request, *args, **kwargs)

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
```

В `forms.py` добавляем форму для создания автомобиля:

```python
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['number', 'brand', 'model', 'color']
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': 'А123ВС77'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Toyota'}),
            'model': forms.TextInput(attrs={'placeholder': 'Camry'}),
            'color': forms.TextInput(attrs={'placeholder': 'Черный'}),
        }
        labels = {
            'number': 'Гос номер',
            'brand': 'Марка',
            'model': 'Модель', 
            'color': 'Цвет',
        }
```

`car_create.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Добавление автомобиля</title>
</head>
<body>
    <div class="nav-links">
        <a href="{% url 'owners' %}">Все владельцы</a>
        <a href="{% url 'cars' %}">Все автомобили</a>
    </div>

    <h1>🚗 Добавление автомобиля</h1>

    <div class="form-container">
        <form method="post">
            {% csrf_token %}
            
            <div class="form-group">
                <label for="id_number">Гос номер:</label>
                {{ form.number }}
                {% if form.number.errors %}
                <div class="error">{{ form.number.errors }}</div>
                {% endif %}
            </div>
            
            <div class="form-group">
                <label for="id_brand">Марка:</label>
                {{ form.brand }}
                {% if form.brand.errors %}
                <div class="error">{{ form.brand.errors }}</div>
                {% endif %}
            </div>
            
            <div class="form-group">
                <label for="id_model">Модель:</label>
                {{ form.model }}
                {% if form.model.errors %}
                <div class="error">{{ form.model.errors }}</div>
                {% endif %}
            </div>

            <div class="form-group">
                <label for="id_color">Цвет:</label>
                {{ form.color }}
                {% if form.color.errors %}
                <div class="error">{{ form.color.errors }}</div>
                {% endif %}
            </div>

            <button type="submit" class="btn">🚗 Добавить автомобиль</button>
            <a href="{% url 'cars' %}" class="btn-cancel">❌ Отмена</a>
        </form>
    </div>
</body>
</html>
```

`car_delete.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Удаление владельца</title>
</head>
<body>
    <div class="nav-links">
        <a href="{% url 'owners' %}">Все владельцы</a>
        <a href="{% url 'cars' %}">Все автомобили</a>
    </div>

    <h1>Удаление владельца</h1>

    <div class="delete-container">
        <div class="warning-message">
            <strong>⚠️ Внимание!</strong> Вы собираетесь удалить владельца. Это действие нельзя отменить.
        </div>

        <div class="owner-info">
            <p><strong>Владелец для удаления:</strong></p>
            <p><strong>ID:</strong> {{ owner.owner_id }}</p>
            <p><strong>Фамилия:</strong> {{ owner.surname }}</p>
            <p><strong>Имя:</strong> {{ owner.name }}</p>
            <p><strong>Дата рождения:</strong> {{ owner.birth_date }}</p>
        </div>

        <form method="post">
            {% csrf_token %}
            <p>Вы уверены, что хотите удалить этого владельца?</p>
            <button type="submit" class="btn btn-danger">🗑️ Да, удалить</button>
            <a href="{% url 'owners' %}" class="btn btn-secondary">❌ Отмена</a>
        </form>
    </div>
</body>
</html>
```

В `urls.py` добавляем новые пути:

```python 
path('owners/create/', views.create_owner, name='owner_form'),
path('cars/create/', views.create_car, name='car_create'),
path('cars/<int:car_id>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
```