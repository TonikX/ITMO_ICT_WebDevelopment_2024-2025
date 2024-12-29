  Документация: Панель управления (Dashboard)

# Панель управления (Dashboard)

Панель управления зависит от роли пользователя: студента или преподавателя. Каждый из них имеет доступ к отдельным функциям и данным в системе. В этой документации описано, как происходит авторизация и маршрутизация для обоих типов пользователей.

## URL-маршруты для Dashboard

Маршруты для страницы `dashboard` и других связанных разделов настроены в файле `urls.py`.

```
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
    path('homeworks/', views.HomeworkListView.as_view(), name='homework_list'),
    path('student/homeworks/', views.StudentHomeworkListView.as_view(), name='student_homeworks'),
    path('homeworks/create/', views.HomeworkCreateView.as_view(), name='homework_create'),
    path('homeworks//submit/', views.SubmissionCreateView.as_view(), name='submit_homework'),
    path('homeworks/list/submissions/', views.SubmissionListView.as_view(), name='submission_list'),
    path('homeworks/submission//grade/', views.SubmissionGradeView.as_view(), name='grade_submission'),
    path('grades/admin/', views.AdminGradeTableView.as_view(), name='admin_grade_table'),
    path('grades/student/', views.StudentGradeTableView.as_view(), name='student_grade_table')
]
```

## Описание функций и классов, используемых в панели управления

### Функции панели управления для студента

*   **Просмотр заданий**: Студенты могут увидеть все домашние задания, доступные для выполнения, через маршрут `student/homeworks/` и `StudentHomeworkListView` в `views.py`.
*   **Отправка выполненного задания**: Студенты могут прикрепить выполнение задания через маршрут `homeworks/<int:homework_id>/submit/`, который связан с `SubmissionCreateView`.
*   **Просмотр оценок**: Через маршрут `grades/student/` и `StudentGradeTableView`, студенты могут просматривать свои оценки.

### Функции панели управления для преподавателя

*   **Добавление нового задания**: Преподаватели могут создавать новые задания через маршрут `homeworks/create/` и `HomeworkCreateView`.
*   **Проверка и оценка выполнения заданий**: Через маршрут `homeworks/list/submissions/` преподаватели могут видеть выполненные студентами задания и выставлять оценки с помощью `SubmissionGradeView`.
*   **Управление предметами**: Преподаватели могут добавлять и редактировать предметы через маршруты `subjects/add/` и `subjects/<int:pk>/edit/`.
*   **Просмотр оценок всех студентов**: Через маршрут `grades/admin/` преподаватели могут просматривать таблицу с оценками всех студентов.

## Класс `UserDashboardView` для панели управления

Класс `UserDashboardView` реализует общую панель для студентов и преподавателей. Он отображает только те элементы, которые доступны по роли пользователя, проверяя `role` пользователя в базе данных.

```
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Submission

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

### Ключевые функции `UserDashboardView`

*   **`get_queryset`**: Метод возвращает список заданий для студента или преподавателя в зависимости от роли. Если авторизован студент, отображаются только его задания. Если преподаватель, то задания всех студентов, проходящих его курсы.
*   **`get_context_data`**: Метод добавляет дополнительный контекст `is_student` для проверки в шаблоне, чтобы различать отображаемые функции для студентов и преподавателей.

## Шаблон `dashboard.html`

Шаблон `dashboard.html` проверяет роль пользователя через `is_student` и отображает соответствующие функции в зависимости от роли. Например, кнопка "Добавить задание" отображается только преподавателям, а студентам доступны кнопки для отправки выполненного задания.

### Шаблон

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Панель управления</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    {% include 'navbar.html' %}
    <div class="container mt-5">
        <h2 class="mb-4 text-center">Панель управления</h2>

        <div class="card mb-4">
            <div class="card-body">
                <h4 class="card-title">Профиль пользователя</h4>
                <p><strong>Имя пользователя:</strong> {{ user.username }}</p>
                <p><strong>Email:</strong> {{ user.email }}</p>
                <p><strong>Роль:</strong> {{ user.role }}</p>
            </div>
        </div>

        {% if is_student %}
            <h4>Ваши домашние задания и оценки:</h4>

            <a href="{% url 'student_grade_table' %}" class="btn btn-primary mb-3">Мои оценки</a>

            <a href="{% url 'student_homeworks' %}" class="btn btn-info mb-3">Просмотр заданий</a>

            <a href="{% url 'submit_homework' homework_id=1 %}" class="btn btn-success mb-3">Прикрепить задание</a> 

        {% else %}
            <h4>Оценки всех студентов:</h4>

            <a href="{% url 'admin_grade_table' %}" class="btn btn-primary mb-3">Оценки всех студентов</a>
            
            <a href="{% url 'submission_list' %}" class="btn btn-info mb-3">Управление заданиями</a>
        {% endif %}

        {% if submissions %}
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Ученик</th>
                        {% if not is_student %}
                            <th>Класс</th>
                        {% endif %}
                        <th>Задание</th>
                        <th>Дата сдачи</th>
                        <th>Оценка</th>
                    </tr>
                </thead>
                <tbody>
                    {% for submission in submissions %}
                        <tr>
                            <td>{{ submission.student.username }}</td>
                            {% if not is_student %}
                                <td>{{ submission.student.student_class.name }}</td>
                            {% endif %}
                            <td>{{ submission.homework.subject.name }}</td>
                            <td>{{ submission.submitted_at|date:"d.m.Y H:i" }}</td>
                            <td>{{ submission.grade|default:"Не оценено" }}</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% else %}
            <p class="alert alert-warning">Нет данных о сдачах заданий.</p>
        {% endif %}
    </div>
</body>
</html>
```

## Маршрутизация и взаимодействие

*   После входа пользователя через `login` он перенаправляется на `dashboard`, где доступные функции зависят от роли.
*   Каждый маршрут, относящийся к панели управления, имеет соответствующее представление и шаблон, определяющий, какие функции доступны.