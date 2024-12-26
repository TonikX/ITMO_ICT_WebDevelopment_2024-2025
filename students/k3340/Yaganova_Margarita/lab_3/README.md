# django-rest-api
API REST, написанный на Django

## Используемые технологии
* [Django](https://www.djangoproject.com/): Веб-фреймворк для перфекционистов с жесткими сроками (Django создает лучшие веб-приложения с меньшим количеством кода).
* [DRF](www.django-rest-framework.org/): Мощный и гибкий набор инструментов для создания веб-API

* #### Зависимости
     1. Установите зависимости, необходимые для запуска приложения:
        ```bash
            $ pip install django djangorestframework djoser django_filters drf_yasg django-cors-headers
        ```
     2. Запустите миграции:
        ```bash
            $ python manage.py makemigrations
            $ python manage.py migrate
        ```

* #### Let's go!
    Запустите сервер с помощью этой простой команды:
    ```bash
        $ python manage.py runserver
    ```
    Теперь вы можете получить доступ к службе API файлов в своем браузере, используя
    ```
        http://127.0.0.1:8000/admin/
        http://127.0.0.1:8000/api/
        http://127.0.0.1:8000/auth/
    ```
