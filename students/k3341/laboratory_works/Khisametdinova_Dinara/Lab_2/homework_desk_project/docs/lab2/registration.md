# Регистрация пользователя

## Описание

Функция регистрации позволяет пользователям создать новый аккаунт в системе. Пользователь может выбрать свою роль — "студент" или "учитель". Интерфейс регистрации представлен в шаблоне `registration.html`, где используется стиль `Bootstrap` для оформления и кастомные стили, чтобы создать удобную и интуитивно понятную форму регистрации.

## Шаблон `registration.html`

Форма регистрации включает поля для ввода имени пользователя, имени, электронной почты, пароля, повторного пароля и роли пользователя.

### Код шаблона

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Регистрация нового пользователя</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        .form-container {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        }
        .form-header {
            text-align: center;
            font-weight: bold;
            color: #343a40;
            margin-bottom: 30px;
        }
        .btn-custom {
            background-color: #007bff;
            border-color: #0056b3;
            color: #fff;
            width: 100%;
            margin-top: 20px;
            padding: 12px;
            font-size: 18px;
        }
        .btn-custom:hover {
            background-color: #0056b3;
            border-color: #003d80;
        }
        .form-control:focus {
            border-color: #007bff;
            box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
        }
        .text-danger {
            font-size: 14px;
        }
    </style>
</head>
<body>
    {% load widget_tweaks %}
    <div class="container mt-5">
        <div class="form-container">
            <h2 class="form-header">Регистрация нового пользователя</h2>
            <form method="post">
                {% csrf_token %}

                <div class="form-group">
                    <label for="username">Имя пользователя</label>
                    {{ form.username|add_class:"form-control" }}
                    {% if form.username.errors %}
                        <div class="text-danger">{{ form.username.errors }}</div>
                    {% endif %}
                </div>

                <div class="form-group">
                    <label for="first_name">Имя</label>
                    {{ form.first_name|add_class:"form-control" }}
                    {% if form.first_name.errors %}
                        <div class="text-danger">{{ form.first_name.errors }}</div>
                    {% endif %}
                </div>

                <div class="form-group">
                    <label for="email">Email</label>
                    {{ form.email|add_class:"form-control" }}
                    {% if form.email.errors %}
                        <div class="text-danger">{{ form.email.errors }}</div>
                    {% endif %}
                </div>

                <div class="form-group">
                    <label for="password">Пароль</label>
                    {{ form.password|add_class:"form-control" }}
                    {% if form.password.errors %}
                        <div class="text-danger">{{ form.password.errors }}</div>
                    {% endif %}
                </div>

                <div class="form-group">
                    <label for="password2">Повторите пароль</label>
                    {{ form.password2|add_class:"form-control" }}
                    {% if form.password2.errors %}
                        <div class="text-danger">{{ form.password2.errors }}</div>
                    {% endif %}
                </div>

                <div class="form-group">
                    <label for="role">Роль</label>
                    {{ form.role|add_class:"form-control" }}
                    {% if form.role.errors %}
                        <div class="text-danger">{{ form.role.errors }}</div>
                    {% endif %}
                </div>

                <button type="submit" class="btn btn-custom">Зарегистрироваться</button>
            </form>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```
### Ключевые элементы шаблона

*   **Имя пользователя (username):** Поле для ввода уникального имени пользователя.
*   **Имя (first\_name):** Поле для ввода имени пользователя.
*   **Email:** Поле для ввода электронной почты.
*   **Пароль (password) и Повтор пароля (password2):** Два поля для ввода пароля и его подтверждения.
*   **Роль (role):** Поле выбора, которое позволяет выбрать роль пользователя, `student` или `teacher`.


Класс RegistrationView обрабатывает отображение и логику регистрации нового пользователя. Он наследует CreateView и использует UserRegistrationForm для валидации данных пользователя. После успешной регистрации пользователя перенаправляет на страницу входа.

```python
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegistrationForm
from .models import User

class RegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')
```

### Основные функции

*   **`model`:** Модель `User`, которая будет использоваться для создания нового пользователя.
*   **`form_class`:** Форма `UserRegistrationForm`, определяющая поля и валидацию для регистрации.
*   **`template_name`:** Указание шаблона `registration.html`.
*   **`success_url`:** Адрес, куда будет перенаправлен пользователь после успешной регистрации (страница входа).

## Форма `UserRegistrationForm`

Форма `UserRegistrationForm` содержит поля для всех необходимых данных пользователя, включая проверку совпадения паролей.

### Код для формы

```python
from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'role']

    def clean_password2(self):
        cd = self.cleaned_data
```


