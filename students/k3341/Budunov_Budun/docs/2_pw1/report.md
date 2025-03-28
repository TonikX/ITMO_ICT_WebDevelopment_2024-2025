# Отчет по практической работе №1

## Пункт 1

Проект состоит из трех основных файлов:

- `models.py` - определение моделей данных с использованием Pydantic
- `temp_db.py` - временная база данных с тестовыми данными
- `main.py` - основной файл приложения с API-эндпоинтами

Модели данных (Pydantic)

В файле `models.py` определены модели данных с использованием библиотеки Pydantic. Pydantic обеспечивает валидацию данных, сериализацию/десериализацию и документирование моделей.

```python
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

class Category(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class Task(BaseModel):
    id: int
    description: str
    priority: int
    user: Optional[User] = None
    category: Optional[Category] = None
```

Преимущества использования Pydantic:

- Строгая типизация данных
- Валидация данных
- Документация моделей
- Поддержка вложенных моделей 
- Сериализация/десериализация данных

Временная база данных

Файл `temp_db.py` содержит тестовые данные для демонстрации работы API:

```python
# Users data
users_db = [
    {
        "id": 1,
        "username": "admin",
        "is_active": True,
        "is_admin": True
    },
    # ...
]

# Categories data
categories_db = [
    {
        "id": 1,
        "name": "Work",
        "description": "Work-related tasks"
    },
    # ...
]

# Tasks data
tasks_db = [
    {
        "id": 1,
        "description": "Complete project report",
        "priority": 1,
        "user": users_db[0],
        "category": categories_db[0]
    },
    # ...
]
```
API-эндпоинты

В файле `main.py` определены API-эндпоинты для работы с данными.

```python
@app.get("/users/", response_model=List[User], tags=["Users"])
def get_users():
    return users_db
```

Аннотация эндпоинтов

Все эндпоинты аннотированы с использованием типов Python и специальных параметров FastAPI:

1. `response_model` - указывает тип данных, которые должны быть возвращены
2. Параметр пути - `user_id` - указывает, что этот эндпоинт принимает параметр пути
3. Параметр запроса - `priority` - указывает, что этот эндпоинт принимает параметр запроса
4. Тело запроса - `user: User`

Основные группы эндпоинтов

Пользователи (Users):

- `GET /users/` - получение списка всех пользователей
- `GET /users/{user_id}` - получение информации о пользователе по его ID
- `POST /users/` - создание нового пользователя
- `PUT /users/{user_id}` - обновление информации о пользователе
- `DELETE /users/{user_id}` - удаление пользователя

Категории (Categories):

- `GET /categories/` - получение списка всех категорий
- `GET /categories/{category_id}` - получение информации о категории по ее ID
- `POST /categories/` - создание новой категории
- `PUT /categories/{category_id}` - обновление информации о категории
- `DELETE /categories/{category_id}` - удаление категории

Задачи (Tasks):

- `GET /tasks/` - получение списка всех задач
- `GET /tasks/{task_id}` - получение информации о задаче по ее ID
- `POST /tasks/` - создание новой задачи
- `PUT /tasks/{task_id}` - обновление информации о задаче
- `DELETE /tasks/{task_id}` - удаление задачи
- `GET /users/{user_id}/tasks/` - получение списка задач пользователя по его ID

Ссылка на коммит с кодом: [.../practical_works/sem2_practice_1](https://github.com/budun-ov/ITMO_ICT_WebDevelopment_2024-2025/commit/2ad06b829a74a8fb4b920a780d9e8cefa36dc02e)

## Пункт 2

Подключение к БД:

```python
from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
engine = create_engine(db_url, echo=True)  # echo=True для логирования SQL-запросов

# Функция для создания таблиц
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Функция для получения сессии
def get_session():
    with Session(engine) as session:
        yield session
```

Создание моделей: 

Итоговые модели можно посмотреть в файле [models.py](https://github.com/budun-ov/ITMO_ICT_WebDevelopment_2024-2025/blob/sem2_lw-1/students/k3341/Budunov_Budun/laboratory_works/sem2_laboratory_work_1/models.py) лабораторной работы №1.

Запросы тоже можно посмотреть в файле [main.py](https://github.com/budun-ov/ITMO_ICT_WebDevelopment_2024-2025/blob/sem2_lw-1/students/k3341/Budunov_Budun/laboratory_works/sem2_laboratory_work_1/main.py). В них создаем сессии, работаем с данными и указываем схемы для валидации.

## Пункт 3

Читайте пункт `Переменные окружения` в отчете к лабораторной работе №1.