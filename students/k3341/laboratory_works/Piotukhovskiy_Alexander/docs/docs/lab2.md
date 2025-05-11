# Лабораторная работа 2. Реализация простого сайта на django. Вариант 5 (Список научных конференций)

---

## 1. Регистрация
```python
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('conference_list')
    else:
        form = UserCreationForm()
    return render(request, 'authorization/register.html', {'form': form})
```

Шаблон
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Регистрация</title>
    <link rel="stylesheet" href="{% static 'style.css' %}">
</head>
<body>
    <header>
        <h1>Регистрация</h1>
    </header>

    <section>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Зарегистрироваться</button>
        </form>
        <p class="center-text">Уже зарегистрированы? <a href="{% url 'login' %}">Войти</a></p>
    </section>
</body>
</html>
```
В представлении `register` обрабатывается регистрация нового пользователя. Если метод запроса `POST`, форма `UserCreationForm` получает данные. При успешной валидации создается новый пользователь, сразу же выполняется вход, и происходит перенаправление на страницу со списком конференций. Если же метод запроса `GET`, просто отображается пустая форма регистрации.

Шаблон отображает форму регистрации, кнопку «Зарегистрироваться» и ссылку для перехода на страницу входа, если пользователь уже зарегистрирован.

## 2. Авторизация
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Вход</title>
    <link rel="stylesheet" href="{% static 'style.css' %}">
</head>
<body>
    <header>
        <h1>Вход в систему</h1>
    </header>

    <section>
        <form method="post">
            {% if form.errors %}
            <div class="errorlist">
                <li>Неверный логин или пароль</li>
            </div>
        {% endif %}
            {% csrf_token %}
            <label for="username">Имя пользователя:</label>
            <input type="text" id="username" name="username" required>

            <label for="password">Пароль:</label>
            <input type="password" id="password" name="password" required>

            <button type="submit">Войти</button>
        </form>
        <p class="center-text">Впервые на сайте? <a href="{% url 'register' %}">Зарегистрироваться</a></p>
    </section>
</body>
</html>
```
Шаблон авторизации отображает форму для ввода имени пользователя и пароля. Если аутентификация не завершается успехом, выводится сообщение об ошибке «Неверный логин или пароль».

## 3.1. Просмотр всех конференций
```python
def conference_list(request):
    query = request.GET.get('q', '')

    conferences = Conference.objects.all()
    if query:
        conferences = conferences.filter(
            Q(title__icontains=query) |
            Q(topics__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query) |
            Q(participation_conditions__icontains=query)
        )

    conferences = conferences.order_by('-created_at')

    paginator = Paginator(conferences, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page', 1)

    try:
        conferences_page = paginator.page(page_number)
    except PageNotAnInteger:
        conferences_page = paginator.page(1)
    except EmptyPage:
        conferences_page = paginator.page(paginator.num_pages)

    return render(request, 'conferences/conference_list.html', {
        'conferences': conferences_page,
        'paginator': paginator,
        'page_obj': conferences_page,
        'query': query
    })
```

Шаблон
```html
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Список конференций</title>
    <link rel="stylesheet" href="{% static 'style.css' %}">
</head>
<body>
<header>
    <h1>Список научных конференций</h1>
    {% if user.is_authenticated %}
        <p>Вы вошли как {{ user.username }} | <a href="{% url 'logout_redirect' %}">Выйти</a></p>
        <p><a href="{% url 'create_conference' %}" class="btn">Создать новое мероприятие</a></p>
    {% else %}
        <p><a href="{% url 'login' %}">Войти</a> | <a href="{% url 'register' %}">Регистрация</a></p>
    {% endif %}
</header>

<section>
    <form method="get" action="{% url 'conference_list' %}" class="search-form">
        <input type="text" name="q" value="{{ query }}" placeholder="Поиск по конференциям">
        <button type="submit" class="btn">Поиск</button>
    </form>
</section>

<section>
    {% if conferences %}
        <ul>
            {% for conference in conferences %}
                <li>
                    <h2>{{ conference.title }}</h2>
                    <p><strong>Тематика:</strong> {{ conference.topics }}</p>
                    <p><strong>Место:</strong> {{ conference.location }}</p>
                    <p><strong>Даты:</strong> {{ conference.start_date }} - {{ conference.end_date }}</p>
                    <p><strong>Описание:</strong> {{ conference.description }}</p>
                    <p><strong>Условия участия:</strong> {{ conference.participation_conditions }}</p>
                    <p><strong>Дата создания:</strong> {{ conference.created_at|date:"Y-m-d H:i" }}</p>
                    <p><strong>Последнее изменение:</strong> {{ conference.updated_at|date:"Y-m-d H:i" }}</p>


                    <p><a href="{% url 'conference_detail' conference.id %}" class="btn-link">Посмотреть подробности</a>
                    </p>
                    {% if user.is_authenticated %}
                        {% if user != conference.owner %}
                            {% if user in conference.participants.all %}
                                {% if user in conference.ratings.all %}
                                    <p><a href="{% url 'rate_conference' conference.id %}" class="btn-link">Изменить
                                        оценку</a></p>
                                {% else %}
                                    <p><a href="{% url 'rate_conference' conference.id %}" class="btn-link">Оценить</a>
                                    </p>
                                {% endif %}
                                <p><a href="{% url 'cancel_registration' conference.id %}" class="btn-link">Отменить
                                    регистрацию</a></p>
                            {% else %}
                                <p><a href="{% url 'register_for_conference' conference.id %}" class="btn-link">Зарегистрироваться</a>
                                </p>
                            {% endif %}
                        {% endif %}
                    {% endif %}
                </li>
            {% endfor %}
        </ul>

        <div class="pagination">
            {% if conferences.has_previous %}
                <a href="?q={{ query }}&page={{ conferences.previous_page_number }}" class="btn">Предыдущая страница</a>
            {% else %}
                <span class="btn disabled">Предыдущая страница</span>
            {% endif %}

            <span class="page-info">
                    Страница {{ conferences.number }} из {{ conferences.paginator.num_pages }}
                </span>

            {% if conferences.has_next %}
                <a href="?q={{ query }}&page={{ conferences.next_page_number }}" class="btn">Следующая страница</a>
            {% else %}
                <span class="btn disabled">Следующая страница</span>
            {% endif %}
        </div>
    {% else %}
        <p>Конференции не найдены.</p>
    {% endif %}
</section>
</body>
</html>
```

В представлении `conference_list` реализован поиск и пагинация. Сначала считывается поисковый запрос `q`, и, если он задан, выполняется фильтрация конференций по полям `title`, `topics`, `location`, `description` и `participation_conditions`. Затем конференции сортируются по полю `created_at` в порядке убывания.

Пагинация применяется к отфильтрованному списку конференций, используя значение `ITEMS_PER_PAGE` из настроек. Если запрос страницы (`page`) не является числом или превышает количество страниц, выбирается первая или последняя доступная страница. 

Шаблон отображает список конференций с полями, а также данными о входе в аккаунт сверху. Внизу добавлены элементы управления пагинацией, которые сохраняют поисковый запрос и переходят между страницами с учетом текущего фильтра.

## 3.2. Просмотр конференции, редактирование, удаление
```python
def conference_detail(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    user_rating = None
    if request.user.is_authenticated:
        user_rating = ConferenceRating.objects.filter(user=request.user, conference=conference).first()

    return render(request, 'conferences/conference_detail.html', {
        'conference': conference,
        'user_rating': user_rating,
    })


@login_required
def view_participants(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id, owner=request.user)
    participants = conference.participants.all()

    return render(request, 'conferences/view_participants.html',
                  {'conference': conference, 'participants': participants})


@login_required
def create_conference(request):
    if request.method == "POST":
        form = ConferenceForm(request.POST)
        if form.is_valid():
            conference = form.save(commit=False)
            conference.owner = request.user
            conference.save()
            return redirect('conference_list')
    else:
        form = ConferenceForm()
    return render(request, 'conferences/create_conference.html', {'form': form})


@login_required
def edit_conference(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)

    if conference.owner != request.user:
        return redirect('conference_detail', conference_id=conference.id)

    if request.method == "POST":
        form = ConferenceForm(request.POST, instance=conference)
        if form.is_valid():
            form.save()
            return redirect('conference_detail', conference_id=conference.id)
    else:
        form = ConferenceForm(instance=conference)

    return render(request, 'conferences/edit_conference.html', {'form': form, 'conference': conference})
```
В представлении `conference_detail` отображаются подробности конференции, а для авторизованных пользователей загружается их оценка конференции, если она есть. 

В представлении `create_conference` создается новая конференция. Если метод запроса `POST`, форма сохраняется с текущим пользователем как владельцем. При `GET`-запросе отображается пустая форма для создания конференции.

Представление `edit_conference` позволяет владельцу конференции редактировать её данные. Если метод запроса `POST`, данные сохраняются, а при `GET` отображается текущая информация о конференции для редактирования.

Представление `view_participants` проверяет, что текущий пользователь — владелец конференции, и отображает список участников для данной конференции.


## 4. Оставить отзыв на конференцию
```python
@login_required
def rate_conference(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)

    if request.user not in conference.participants.all():
        return redirect('conference_detail', conference_id=conference.id)

    rating = ConferenceRating.objects.filter(user=request.user, conference=conference).first()
    created = rating is None

    if request.method == "POST":
        form = ConferenceRatingForm(request.POST, instance=rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.conference = conference
            rating.save()
            return redirect('conference_detail', conference_id=conference.id)
    else:
        form = ConferenceRatingForm(instance=rating)

    return render(request, 'conferences/rate_conference.html',
                  {'form': form, 'conference': conference, 'created': created})


@login_required
def view_ratings(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id, owner=request.user)
    ratings = ConferenceRating.objects.filter(conference=conference)

    return render(request, 'conferences/view_ratings.html', {'conference': conference, 'ratings': ratings})
```
В представлении `rate_conference` реализована возможность добавления и изменения оценки конференции для участников. Если пользователь не является участником конференции, он перенаправляется на страницу с подробной информацией о конференции. При получении `POST`-запроса данные формы сохраняются, связываясь с текущим пользователем и конференцией. Если форма загружается через `GET`, отображается существующая оценка, если она уже была добавлена.

В представлении `view_ratings` проверяется, что текущий пользователь является владельцем конференции, после чего загружаются и отображаются все оценки участников для данной конференции.


Шаблон оценки
```html
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{% if created %}Оценить{% else %}Изменить оценку{% endif %} конференцию</title>
    <link rel="stylesheet" href="{% static 'style.css' %}">
</head>
<body>
    <header>
        <h1>{% if created %}Оценить{% else %}Изменить оценку{% endif %} конференцию "{{ conference.title }}"</h1>
    </header>

    <section>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">{% if created %}Оценить{% else %}Сохранить изменения{% endif %}</button>
        </form>
        <p><a href="{% url 'conference_detail' conference.id %}" class="btn-link">Вернуться к конференции</a></p>
    </section>
</body>
</html>
```

Шаблон оценки позволяет участникам добавить или изменить оценку конференции. Кнопка меняет текст на «Оценить» при создании новой оценки и на «Сохранить изменения» при редактировании.

## 5. Администратор должен иметь возможность указания результатов выступления
Если пользователь имеет статус суперпользователя, то ему открывается доступ к админ панели, где он может отметить конференцию как рекомендованную к публикации.

## 6. В клиентской части должна формироваться таблица, отображающая всех участников по конференциям
```python
@login_required
def view_participants(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id, owner=request.user)
    participants = conference.participants.all()

    return render(request, 'conferences/view_participants.html',
                  {'conference': conference, 'participants': participants})
```
В `view_participants` загружается конференция, проверяя, что текущий пользователь является её владельцем. Если проверка пройдена, загружается список участников конференции, который затем передается в шаблон `view_participants.html` для отображения.

```html
{% load static %}
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Участники конференции</title>
    <link rel="stylesheet" href="{% static 'style.css' %}">
</head>
<body>
    <header>
        <h1>Участники конференции "{{ conference.title }}"</h1>
    </header>

    <section>
        {% if participants %}
            <ul>
                {% for participant in participants %}
                    <li>{{ participant.username }}</li>
                {% endfor %}
            </ul>
        {% else %}
            <p>Пока нет зарегистрированных участников.</p>
        {% endif %}
        <p><a href="{% url 'conference_detail' conference.id %}" class="btn-link">Вернуться к конференции</a></p>
    </section>
</body>
</html>
```
Шаблон отображает список участников конференции. Если есть зарегистрированные участники, они выводятся списком с именами пользователей. Если участников нет, отображается сообщение об отсутствии зарегистрированных. Внизу страницы добавлена ссылка для возврата на страницу с подробной информацией о конференции.
