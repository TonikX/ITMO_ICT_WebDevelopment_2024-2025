# Авторизация

## Описание

Процесс авторизации позволяет пользователям входить в систему с учетными данными, обеспечивая доступ к личному кабинету и другим защищенным страницам. При успешной авторизации пользователь перенаправляется на `dashboard`, в зависимости от своей роли (учитель или студент), и получает доступ к соответствующим разделам системы. Процесс реализован с использованием Django и шаблона `login.html` для удобного ввода данных пользователя.

## Шаблон `login.html`

Этот шаблон представляет собой простую форму для ввода имени пользователя и пароля. Он использует `Bootstrap` для стилизации и удобства отображения. В шаблоне также предусмотрен вывод ошибок в случае, если пользователь ввел неверное имя пользователя или пароль.

### Код шаблона

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h2 class="mb-4 text-center">Вход в систему</h2>
        <form method="post" class="form-signin">
            {% csrf_token %}
            <div class="form-group">
                <label for="username">Имя пользователя</label>
                <input type="text" name="username" class="form-control" required autofocus>
            </div>
            <div class="form-group">
                <label for="password">Пароль</label>
                <input type="password" name="password" class="form-control" required>
            </div>
            <button class="btn btn-primary btn-block" type="submit">Войти</button>
        </form>

        {% if form.errors %}
            <div class="alert alert-danger mt-3">
                <strong>Ошибка:</strong> Неверное имя пользователя или пароль.
            </div>
        {% endif %}
    </div>
</body>
</html>
```

### Ключевые элементы шаблона

*   **Имя пользователя (username):** Поле для ввода имени пользователя.
*   **Пароль (password):** Поле для ввода пароля.
*   **Кнопка входа:** Кнопка для отправки формы и попытки входа в систему.
*   **Сообщение об ошибке:** Появляется, если введены неверные данные для авторизации.

## Вид для авторизации: `CustomLoginView`

Класс `CustomLoginView` расширяет стандартный `LoginView` Django и используется для обработки процесса входа пользователя. Этот класс назначает шаблон для формы `login.html` и указывает, куда перенаправить пользователя после успешной авторизации.

### Код `CustomLoginView`

```
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        return reverse_lazy('dashboard')
```

### Основные функции

*   **`template_name`:** Указывает на использование шаблона `login.html` для отображения формы.
*   **`form_class`:** Задает форму `CustomAuthenticationForm`, в которой определены поля для ввода данных и их валидация.
*   **`get_success_url`:** Метод возвращает URL-адрес, на который будет перенаправлен пользователь после успешного входа. В данном случае это `dashboard`.

## URL-маршруты

Пути для входа и выхода пользователя настроены в `urls.py`. Вход перенаправляет на `CustomLoginView`, а выход перенаправляет пользователя обратно на страницу входа.

### Код `urls.py`

```
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
```

### Описание маршрутов

*   **`login/`:** URL-адрес для отображения страницы входа. Указывает на `CustomLoginView` и использует шаблон `login.html`.
*   **`logout/`:** URL-адрес для выхода пользователя. После выхода пользователя перенаправляет его на страницу `login`.

## Датафлоу

Когда пользователь заполняет и отправляет форму, данные передаются через `POST`\-запрос на URL `/login/`. Форма отправляется в `CustomLoginView`, который проверяет данные. Если введены корректные имя пользователя и пароль, `get_success_url` перенаправляет пользователя на `dashboard`. В случае ошибки на странице отображается сообщение об ошибке, уведомляющее пользователя о неверных данных.