# Сдача и Оценивание Работ (Submissions)

В системе "Сдача и оценивание работ" представлена раздельная функциональность для студентов и преподавателей. Она включает механизм отправки выполненных заданий студентами и интерфейс для оценки этих работ преподавателями.

## 1\. Страница Сдачи Домашнего Задания

Студенты могут сдавать выполненные задания, перейдя на страницу с адресом `/homeworks/<homework_id>/submit/`. На этой странице студенты видят форму для добавления текста выполнения задания. Шаблон формы `submission.html` выглядит следующим образом:

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Сдача домашнего задания</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h2 class="mb-4">Сдача домашнего задания</h2>
        
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            
            <button type="submit" class="btn btn-primary mt-3">Отправить</button>
        </form>
    </div>
</body>
</html>
```

### Декоратор `student_required`

Для обеспечения безопасности доступа к этому представлению используется декоратор `student_required`, который проверяет роль пользователя. Если роль пользователя — `student`, он может видеть форму сдачи. В противном случае преподаватель перенаправляется к управлению заданиями.

## 2\. Просмотр Выполненных Работ (для преподавателя)

Преподаватели могут просматривать сданные работы на странице `/homeworks/list/submissions/`. Эта страница доступна только преподавателям благодаря декоратору `teacher_required`, который перенаправляет студентов к их списку домашних заданий.

Шаблон `submission_list.html` отображает список сданных работ с возможностью перехода к странице оценивания каждой работы:

```
{% if submissions %}
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Ученик</th>
                <th>Текст выполнения</th>
                <th>Дата сдачи</th>
                <th>Оценка</th>
                <th>Действия</th>
            </tr>
        </thead>
        <tbody>
            {% for submission in submissions %}
                <tr>
                    <td>{{ submission.student.username }}</td>
                    <td>{{ submission.submitted_text }}</td>
                    <td>{{ submission.submitted_at|date:"d.m.Y H:i" }}</td>
                    <td>{{ submission.grade|default:"Не оценено" }}</td>
                    <td>
                        <a href="{% url 'grade_submission' submission.id %}" class="btn btn-warning btn-sm">Оценить</a>
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% endif %}
```

### Класс `SubmissionListView`

Этот класс используется для отображения всех выполненных заданий, доступных преподавателям. Благодаря методу `get_queryset`, `SubmissionListView` получает все объекты `Submission`, связанные с выбранным заданием.

## 3\. Оценивание Выполненных Работ

Преподаватели могут оценивать работы, переходя по ссылке "Оценить" в `submission_list.html`. Эта ссылка ведет на страницу `/homeworks/submission/<submission_id>/grade/`, где преподаватель может видеть полную информацию о сдаче и оставить оценку.

Шаблон `grade_submission.html` позволяет преподавателю выставить оценку:

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Оценить выполнение задания</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h2 class="mb-4">Оценка выполнения задания</h2>
        
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Предмет: {{ submission.homework.subject.name }}</h5>
                <p><strong>Ученик:</strong> {{ submission.student.username }}</p>
                <p><strong>Текст выполнения:</strong> {{ submission.submitted_text }}</p>
                <p><strong>Дата сдачи:</strong> {{ submission.submitted_at|date:"d.m.Y H:i" }}</p>
            </div>
        </div>

        <form method="post" class="mt-4">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary">Сохранить оценку</button>
        </form>
    </div>
</body>
</html>
```

### Класс `SubmissionGradeView`

Класс `SubmissionGradeView` обрабатывает обновление оценки в базе данных. Он наследуется от `UpdateView` и получает объект `Submission` по `submission_id`. Чтобы убедиться, что доступ к оценке имеют только преподаватели, используется метод `test_func`, проверяющий роль пользователя.

После сохранения оценки пользователь перенаправляется обратно на `submission_list`.

## URL-пути и маршрутизация

Взаимодействие между ссылками и представлениями организовано через следующие URL-пути:

*   **Сдача домашнего задания студентом:** `/homeworks/<homework_id>/submit/`
*   **Просмотр списка выполненных заданий (для преподавателей):** `/homeworks/list/submissions/`
*   **Страница для оценки конкретной работы (для преподавателей):** `/homeworks/submission/<submission_id>/grade/`