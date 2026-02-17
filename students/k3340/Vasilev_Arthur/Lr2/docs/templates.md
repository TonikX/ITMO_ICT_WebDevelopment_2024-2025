# Шаблоны (Templates)

## Базовый шаблон (base.html)

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Автогонки{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'race_list' %}">🏎️ Автогонки</a>
            <div class="navbar-nav ms-auto">
                {% if user.is_authenticated %}
                    <a class="nav-link" href="{% url 'user_profile' %}">Профиль</a>
                    <a class="nav-link" href="{% url 'logout' %}">Выход</a>
                {% else %}
                    <a class="nav-link" href="{% url 'login' %}">Вход</a>
                    <a class="nav-link" href="{% url 'register' %}">Регистрация</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

## Список гонок (race_list.html)

```html
{% extends 'racing_app/base.html' %}

{% block title %}Гонки{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <h1>🏁 Доступные гонки</h1>

        {% for race in races %}
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">{{ race.name }}</h5>
                <p class="card-text">{{ race.description|truncatechars:200 }}</p>
                <p class="text-muted">
                    📅 {{ race.date|date:"d.m.Y H:i" }}
                    {% if race.location %}📍 {{ race.location }}{% endif %}
                </p>
                <a href="{% url 'race_detail' race.pk %}" class="btn btn-primary">Подробнее</a>
            </div>
        </div>
        {% empty %}
        <div class="alert alert-info">
            <h4>Нет доступных гонок</h4>
            <p>В данный момент нет активных гонок для регистрации.</p>
        </div>
        {% endfor %}
    </div>

    <div class="col-md-4">
        {% if user.is_authenticated %}
        <div class="card">
            <div class="card-header">
                <h5>Мои регистрации</h5>
            </div>
            <div class="card-body">
                <a href="{% url 'user_profile' %}" class="btn btn-outline-primary">Просмотреть профиль</a>
            </div>
        </div>
        {% else %}
        <div class="card">
            <div class="card-header">
                <h5>Присоединиться</h5>
            </div>
            <div class="card-body">
                <p>Зарегистрируйтесь, чтобы участвовать в гонках!</p>
                <a href="{% url 'register' %}" class="btn btn-success">Регистрация</a>
            </div>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

## Детали гонки (race_detail.html)

```html
{% extends 'racing_app/base.html' %}

{% block title %}{{ race.name }}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h1>{{ race.name }}</h1>
            </div>
            <div class="card-body">
                <p>{{ race.description }}</p>
                <div class="row">
                    <div class="col-sm-6">
                        <strong>Дата и время:</strong><br>
                        {{ race.date|date:"d.m.Y H:i" }}
                    </div>
                    {% if race.location %}
                    <div class="col-sm-6">
                        <strong>Место проведения:</strong><br>
                        {{ race.location }}
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>

        <!-- Регистрация -->
        {% if user.is_authenticated %}
        <div class="card mt-3">
            <div class="card-header">
                <h5>Регистрация на гонку</h5>
            </div>
            <div class="card-body">
                <form method="post" action="{% url 'race_register' race.pk %}">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-success">Зарегистрироваться</button>
                </form>
            </div>
        </div>
        {% endif %}

        <!-- Комментарии -->
        <div class="card mt-3">
            <div class="card-header">
                <h5>Комментарии и отзывы</h5>
            </div>
            <div class="card-body">
                {% for comment in comments %}
                <div class="media mb-3">
                    <div class="media-body">
                        <h6 class="mt-0">{{ comment.author.get_full_name }}</h6>
                        <p>{{ comment.text }}</p>
                        <small class="text-muted">
                            {{ comment.created_date|date:"d.m.Y H:i" }} |
                            Рейтинг: {{ comment.rating }}/10 |
                            Тип: {{ comment.get_type_display }}
                        </small>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- Добавить комментарий -->
        {% if user.is_authenticated %}
        <div class="card mt-3">
            <div class="card-header">
                <h5>Добавить комментарий</h5>
            </div>
            <div class="card-body">
                <form method="post" action="{% url 'add_comment' race.pk %}">
                    {% csrf_token %}
                    <div class="form-group">
                        <label for="id_text">Текст комментария:</label>
                        <textarea class="form-control" id="id_text" name="text" rows="3" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="id_type">Тип комментария:</label>
                        <select class="form-control" id="id_type" name="type">
                            <option value="RACE">Вопрос о гонках</option>
                            <option value="COOP">Вопрос о сотрудничестве</option>
                            <option value="OTHER">Иное</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="id_rating">Рейтинг (1-10):</label>
                        <input type="number" class="form-control" id="id_rating" name="rating" min="1" max="10" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Отправить</button>
                </form>
            </div>
        </div>
        {% endif %}
    </div>

    <div class="col-md-4">
        <!-- Результата гонки -->
        {% if race.registrations.exists %}
        <div class="card">
            <div class="card-header">
                <h5>Результаты гонки</h5>
            </div>
            <div class="card-body">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Позиция</th>
                            <th>Участник</th>
                            <th>Время</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for registration in race.registrations.all %}
                        <tr>
                            <td>{{ registration.position|default:"-" }}</td>
                            <td>{{ registration.racer.get_full_name }}</td>
                            <td>{{ registration.final_time|default:"-" }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
```