# Навигационное меню (Navbar)

Навигационное меню или `navbar` в данном проекте различается для двух типов пользователей: студента и преподавателя. Меню предоставляет доступ к различным функциям системы в зависимости от роли пользователя.

## HTML-код для Navbar

HTML-код для навигационной панели находится в `navbar.html` и использует шаблонные теги Django для отображения ссылок, в зависимости от того, какой пользователь авторизован.

```
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
        <a class="navbar-brand" href="{% url 'dashboard' %}">Система домашних заданий</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'dashboard' %}">Панель управления</a>
                </li>
                {% if user.is_authenticated %}
                    {% if user.role == 'teacher' %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'admin_grade_table' %}">Оценки всех студентов</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'submission_list' %}">Управление заданиями</a>
                        </li>
                    {% endif %}
                    <li class="nav-item">
                        <form method="post" action="{% url 'logout' %}" style="display:inline;">
                            {% csrf_token %}
                            <button type="submit" class="btn btn-link nav-link" style="display:inline; cursor:pointer;">Выйти</button>
                        </form>
                    </li>
                {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'login' %}">Войти</a>
                    </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>
```

## Пояснение функций и маршрутов Navbar

### Ссылки в навигационном меню

Меню отображает разные ссылки, в зависимости от роли пользователя:

*   **Ссылка на панель управления:** `{% url 'dashboard' %}` — доступна всем авторизованным пользователям и направляет на общую панель, которая отображает нужные функции в зависимости от роли.
*   **Ссылка на оценки всех студентов:** `{% url 'admin_grade_table' %}` — доступна только преподавателям и отображает список всех оценок студентов. Студенты не видят эту ссылку в меню.
*   **Ссылка на управление заданиями:** `{% url 'submission_list' %}` — также доступна только преподавателям для проверки выполненных студентами заданий и выставления оценок.
*   **Форма выхода:** реализована через `<form>` для отправки POST-запроса на URL `{% url 'logout' %}`, который завершает сессию пользователя и перенаправляет на страницу входа.

### Логика авторизации

Навигационное меню проверяет, авторизован ли пользователь через условие `user.is_authenticated`. Если пользователь не авторизован, в меню отображается ссылка для входа `{% url 'login' %}`.

## Взаимодействие с представлениями

Роли пользователей обрабатываются во вьюшке `UserDashboardView` и других представлениях, которые фильтруют информацию в зависимости от роли:

```
class UserDashboardView(LoginRequiredMixin, ListView):
    template_name = 'dashboard.html'
    context_object_name = 'submissions'
    
    def get_queryset(self): 
        user = self.request.user
        if user.role == 'student':
            return Submission.objects.filter(student=user).select_related('homework')
        return Submission.objects.filter(homework__subject__teachers=user).select_related('homework', 'student')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_student'] = user.role == 'student'
        return context
```

Методы `get_queryset()` и `get_context_data()` фильтруют данные по роли, возвращая список заданий для студента или списка всех выполненных работ для преподавателя.

## Пример шаблона Navbar с условной логикой

В этом шаблоне отображается меню с ролями и фильтрацией, а также форма для выхода. Таким образом, пользователи видят только те элементы, которые им доступны в зависимости от их роли.