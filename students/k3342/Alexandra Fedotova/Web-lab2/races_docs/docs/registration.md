# Страница регистрации пользователя 

Была реализована регистрация пользователя - он заполняет стандартную форму (вводит ник, почту и пароль). Роль по умолчанию установлена для участника - в моей реализации пользователь может как регистрироваться на гонки, так и оставлять комментарии одновременно.

## Модель юзера
Реализована с помощью AbstractUser, с выбором роли в последующем представлении и форме регистрации.

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('participant', 'Участник'),  
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')

    def is_participant(self):
        return self.role == 'participant'
```

## Представление регистрации

Cоздаем базовое представление регистрации через использование формы. Регистрация производится через POST, затем при выборе роли "участник" пользователя перебрасывает в личный кабинет.

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)

            # Создаем профиль участника
            if user.role == 'participant':
                experience = form.cleaned_data.get('experience')
                Participant.objects.create(user=user, experience=experience)

            # Перенаправляем в личный кабинет
            return redirect('participant_dashboard')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
```

## Форма регистрации 

Создаем форму регистрацию с помощью базовой формы django (UserCreationForm). Добавляем выбор роли пользователя и просим его заранее ввести свой опыт в годах для коррекной работы. Остальные поля (ник, почта и пароль) - поля стандартной регистрации. 

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm 

class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)
    experience = forms.IntegerField(label="Опыт (в годах)", min_value=0, required=True) 

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "role", "experience"] 
```

## HTML-страница регистрации

Я попыталась сделать оформление в стиле Формулы-1, поэтому основные цвета - белый, красный, черный. Страница представляет собой обычное окно-форму для ввода данных. 

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Регистрация на гонки</title>
    <style>
        body {
            background-color: #333;
            font-family: Arial, sans-serif;
            color: #fff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-image: radial-gradient(circle, #333 20%, #222 80%);
        }
        
        .form-container {
            background-color: #222;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.5);
            width: 350px;
            text-align: center;
            border: 2px solid #e10600; 
        }
        
        h2 {
            font-size: 2em;
            color: #e10600; 
            margin: 0 0 15px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .form-container input[type="text"],
        .form-container input[type="email"],
        .form-container input[type="password"] {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            border-radius: 5px;
            border: none;
            outline: none;
            background-color: #333;
            color: #fff;
        }
        
        .form-container button {
            width: 100%;
            padding: 12px;
            background-color: #e10600; 
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }

        .form-container button:hover {
            background-color: #ff1e00;
        }
        
        input::placeholder {
            color: #aaa;
        }
    </style>
</head>
<body>


    <div class="form-container">
        <h2>Регистрация</h2>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Зарегистрироваться</button>
        </form>
    </div>


</body>
</html>
```