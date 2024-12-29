# Практическая работа №3.3

## Задание

Цель работы: овладеть навыками написания документации к API.<br>
Необходимо выполнить все задания с пометкой **"Практическое задание"** [из практической работы №3.3](https://docs.google.com/document/d/1rIfREFvCB4pp8uF990Tz3PLXRJ5u_w-Y3vLxfXWKoxg/edit?usp=sharing).<br> 
Результаты практики загружаются в репозиторий вместе с лабораторной работой.

## Code

```
pip install drf_yasg
```

settings.py:
```python
INSTALLED_APPS = [
  ...,
  'drf_yasg'
]
```

urls.py:
```python
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
Создаем view
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
    ...,
    path('doc/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
```