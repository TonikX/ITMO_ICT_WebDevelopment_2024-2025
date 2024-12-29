# Warriors API

## Описание проекта
**Warriors API** — это RESTful API для управления информацией о воинах, их профессиях и навыках. Проект создан с использованием фреймворка **Django** и **Django REST Framework**.

API поддерживает следующие функции:
- Просмотр всех войнов и их профессий.
- Просмотр всех войнов и их навыков.
- Получение полной информации о войне (по ID), включая профессию и навыки.
- Удаление война по ID.
- Редактирование информации о войне.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/fuetser/ITMO_ICT_WebDevelopment_2024-2025.git
   cd students/k3341/practical_works/Zakharchuk_Aleksandr/warriors_project
    ```

2. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4. Выполните миграции базы данных:
    ```bash
    python manage.py migrate
    ```

5. Запустите сервер:
    ```bash
    python manage.py runserver
    ```

## Используемые технологии

- Python 3.12
- Django
- Django REST Framework
- SQLite
