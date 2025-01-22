## Документация проекта: Создание и настройка системы конференций с использованием Django и Django REST Framework

### Введение

Этот документ описывает шаги по созданию и настройке системы управления научными конференциями с помощью Django и Django REST Framework. Проект будет включать модели данных, API для взаимодействия с фронтендом, аутентификацию пользователей и интерфейс для организации конференций.

### Шаг 1: Настройка проекта Django

1. **Создайте новый проект Django**:
   - Установите Django, если оно еще не установлено, и создайте новый проект.

```bash
django-admin startproject myproject
```

2. **Создайте новое приложение**:
   - Создайте приложение для управления пользователями и конференциями, например, `conferences`.

```bash
python manage.py startapp conferences
```

3. **Добавьте приложение в `INSTALLED_APPS`**:
   - В `settings.py` добавьте созданное приложение в список установленных приложений.

```python
INSTALLED_APPS = [
    # ...
    'conferences',
    'rest_framework',
    'djoser',
    'rest_framework.authtoken',
]
```

### Шаг 2: Определение моделей данных

Определите модели данных для конференций, местоположений, регистраций и других сущностей.

**Пример `models.py` в `conferences`**:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

# Расширенная модель User
class CustomUser(AbstractUser):
    birthday = models.DateField(null=True, blank=True)
    work_education = models.CharField(max_length=100, blank=True)

class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=512)
    description = models.TextField()

    def __str__(self):
        return self.name

class Conference(models.Model):
    title = models.CharField(max_length=255)
    topics = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.title

class ParticipationCondition(models.Model):
    conference = models.OneToOneField(Conference, on_delete=models.CASCADE)
    conditions = models.TextField()

    def __str__(self):
        return f'Conditions for {self.conference.title}'

class Registration(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} registered for {self.conference.title}'

class Review(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.conference.title}'

class PresentationResult(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE)
    is_recommended_for_publication = models.BooleanField(default=False)

    def __str__(self):
        return f'Result for {self.registration}'
```

### Шаг 3: Настройка пользовательской модели и сериализаторов

1. **Используйте кастомную модель пользователя**:
   - В `settings.py` добавьте:

```python
AUTH_USER_MODEL = 'conferences.CustomUser'
```

2. **Создайте сериализаторы для API**:
   - В `serializers.py` создайте сериализаторы для всех моделей.

```python
from rest_framework import serializers
from .models import Location, Conference, ParticipationCondition, Registration, Review, PresentationResult, CustomUser

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'birthday', 'work_education')
        required_fields = ('username', 'password', 'email', 'first_name', 'last_name')

# Создание сериализаторов для других моделей
# Пример для Conference
class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = '__all__'
```

### Шаг 4: Создание API на основе Django REST Framework

1. **Создайте ViewSets для моделей**:
   - В `views.py` создайте ViewSets для обработки запросов.

```python
from rest_framework import viewsets
from .models import Location, Conference, ParticipationCondition, Registration, Review, PresentationResult, CustomUser
from .serializers import ConferenceSerializer, CustomUserCreateSerializer

class ConferenceViewSet(viewsets.ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer
```

2. **Конфигурирование маршрутов для API**:
   - В `urls.py` зарегистрируйте маршруты для всех ViewSet.

```python
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'conferences', views.ConferenceViewSet)

urlpatterns = [
    # другие маршруты
    path('', include(router.urls)),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
```

### Шаг 5: Настройка и регистрация пользователей через Djoser

1. **Настройка Djoser для аутентификации**:
   - Убедитесь, что Djoser настроен в `settings.py`.

```python
DJOSER = {
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SERIALIZERS': {
        'user_create': 'conferences.serializers.CustomUserCreateSerializer',
    },
}
```

### Шаг 6: Создание интерфейса с пагинацией и фильтрацией

1. **Используйте Django Templates и DRF**:
   - Создайте фронтенд с использованием шаблонов Django или интегрируйте с фронтендом на любом нужном вам фреймворке.

2. **Настройте пагинацию и фильтрацию**:
   - Добавьте пагинацию в `settings.py`.

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

### Шаг 7: Создание документации API

1. **Установите и настройте drf-yasg для Swagger**:
   - Установите drf-yasg и добавьте маршруты для Swagger документации.

```bash
pip install drf-yasg
```

2. **Настройте Swagger в `urls.py`**:

```python
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Conference API",
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
```

### Заключение

В результате мы получили REST API сервис для нашей задачи, и научились делать это в django.