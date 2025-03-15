# Практическая работа 3

## Задание 1

1. Составить README файл для описания проекта.
2. Внедрить Swagger в проект.
3. Инициализировать MKdocs с тремя страницами описывающими общее описание проекта в репозитории, трех ендпоинтов, существующих в проекте, регистрации, авторизации и изменения учетных данных пользователя.

README.md

```markdown
# Simple DRF project

## Usage

``python manage.py runserver``

## Project Models

### Warrior

- race - раса война (s - студент, d - разработчик, t - тимлидер)
- name - имя война (CharField, макс.длина=120)
- level - уровень война (IntegerField)
- skill - способности война (ManyToManyField с таблицей Skill, через таблица SkillOfWarrior)
- profession - профессия война (ForeignKey на таблицу Profession)

### Profession

- title - название профессии (CharField, макс.длина=120)
- description - описание профессии (TextField)

### Skill

- title - название способности(CharField, макс.длина=120)

### SkillOfWarrior

- skill - способность (ForeignKey на таблицу Skill)
- warrior - воин (ForeignKey на таблицу Warrior)
- level - уровень способности(IntegerField)

## Views

- ProfessionAPICreate - создание профессии
- SkillAPICreate - создание способности
- SkillAPIView - просмотр способности по id
- WarriorListAPIView - список войнов
- WarriorAPIView - просмотр, изменение и удаление война по id

## Documentation

Available on /doc/swagger
```

Подключение сваггера:

Сперва подключаем сваггер в виртуальное окружение

```terminal
./.venv/Scripts/activate
pip install drf_yasg
```

Добавляем сваггер в подключенные приложения

settings.py

```python
...
INSTALLED_APPS = [
    ...,
    'drf_yasg',
]
...
```

Добавляем урлы сваггера

urls.py

```python
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import include
from django.contrib import admin
from django.urls import path

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v2',
      description="Description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="hardbeat34@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('war/', include('warrior_app.urls')),
    path('doc/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

MKDocs вот прям сейчас читается кекв
