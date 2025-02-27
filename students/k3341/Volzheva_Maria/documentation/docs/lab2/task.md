# Лабораторная работа №2
## Задание:
Реализовать сайт используя фреймворк Django 3 и СУБД PostgreSQL *, в
соответствии с вариантом задания лабораторной работы.

## Мой вариант:
О домашнем задании должна храниться следующая информация: предмет,
преподаватель, дата выдачи, период выполнения, текст задания, информация о штрафах.
Необходимо реализовать следующий функционал:
- Регистрация новых пользователей.
- Просмотр домашних заданий по всем дисциплинам (сроки выполнения,
описание задания).
- Сдача домашних заданий в текстовом виде.
- Администратор (учитель) должен иметь возможность поставить оценку за
задание средствами Django-admin.
- В клиентской части должна формироваться таблица, отображающая оценки
всех учеников класса.

## Описание модели:
#### Модель Class
- Описание: Представляет класс учеников.
- Поля:
  - name: Название класса (строка, макс. длина 100).


#### Модель User
- Описание: Расширенная пользовательская модель, наследованная от AbstractUser.
- Поля:
  - role: Роль пользователя (строка, макс. длина 10, выбор из 'student' или 'teacher', по умолчанию 'student').
  - student_class: Внешний ключ на Class (отображает, к какому классу принадлежит студент).

#### Модель Subject
- Описание: Представляет предметы, которые могут преподаваться.
- Поля:
  - name: Название предмета (строка, макс. длина 100).
  - teachers: Множественное отношение к User, выбирается только среди учителей.
  - description: Описание предмета (текст, допускается пустое значение).


#### Модель Homework
- Описание: Представляет задания по предметам.
- Поля:
  - subject: Внешний ключ на Subject.
  - date_from: Дата начала задания.
  - date_to: Дата окончания задания (типа DateField).
  - description: Описание задания (текст).
  - penalties_info: Информация о штрафах (текст, допускается пустое значение).
  - classes: Множественное отношение к Class, отражающее, для каких классов задается домашнее задание.

#### Модель Submission
- Описание: Представляет сдачу домашнего задания студентом.
- Поля:
  - homework: Внешний ключ на Homework.
  - student: Внешний ключ на User (студента).
  - submitted_text: Текст, предоставленный в качестве решения (текст).
  - submitted_at: Дата и время сдачи (автоматически устанавливается при создании).
  - grade: Оценка за работу (целое число, может быть null).

## Описание функционала сайта:
####  Функционал, доступный всем пользователям:
- 'http://127.0.0.1:8000/' - главная страница с прветствием
- 'http://127.0.0.1:8000/registration/' - страница с регистрацией
- 'http://127.0.0.1:8000/login/' - страница с авторизацией

####  Функционал, доступный пользователем, у которых role = 'student':
- 'http://127.0.0.1:8000/home/' - главная страница авторизованного пользователя с основным функционалом в меню
 (отличается, в зависимости от роли)
- 'http://127.0.0.1:8000/homework/<int:pk>/' - страница для просмотра дз и перехода к странице сдачи дз
- 'http://127.0.0.1:8000/homework/<int:pk>/new_submission/' - страница для сдачи дз
- 'http://127.0.0.1:8000/submission/<int:pk>/' - страница для просмотра сданного дз

####  Функционал, доступный пользователем, у которых role = 'teacher':
- 'http://127.0.0.1:8000/home/' - главная страница авторизованного пользователя с основным функционалом в меню
 (отличается, в зависимости от роли)
- 'http://127.0.0.1:8000/submissions/without-grades/' - страница для просмотра непроверенных дз
- 'http://127.0.0.1:8000/submissions/grade/<int:pk>/' - страница для оценки (проверки) домашнего задания
- 'http://127.0.0.1:8000/grades_for_teacher/' - страница для просмотра оценок учеников по классам

## Рассмотрим один пункт из функционала более подробно:
####  Функционал для страница для сдачи дз:
views.py:
```python
def create_submission_(request, pk):
    try:
        our_user = request.user
        if our_user.role == 'student':
            homework = Homework.objects.get(pk=pk)
            if request.method == 'POST':
                # Получаем оценку из формы (предполагается, что форма отправляется методом POST)
                submitted_text = request.POST.get('submitted_text')
                if submitted_text is not None:
                    Submission.objects.create(homework=homework, student=request.user, submitted_text=submitted_text,
                                              submitted_at=datetime.datetime.now())
                    return redirect('home')

            return render(request, 'create_submission_.html', {'homework': homework, 'our_user': request.user})
        return render(request, 'not_available.html', {'our_user': our_user})
    except Exception as e:
        # Логгирование или обработка ошибки
        raise Http404("Страница не найдена")  # Измените на нужный вам ответ
```
create_submission_.html
```html
{% extends "home.html" %}

{% block content %}
    <div class="container my-4 p-4 bg-light rounded">
        <h1 class="text-primary">Отправка дз:</h1>
        <p class="text-dark"><strong>Текст задания:
        </strong>{{ homework.description }}</p>

        <form method="post" class="mb-3">
            {% csrf_token %}
            <div class="form-group">
                <label for="submitted_text" class="font-weight-bold">Моё дз:</label>
                <input type="text" id="submitted_text" name="submitted_text" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Отправить моё дз</button>
        </form>

        <a href="/submissions/without-grades/" class="btn btn-link">Назад</a>
    </div>
{% endblock %}
```
urls.py
```
urlpatterns = [
    ...
    path('homework/<int:pk>/new_submission/', views.create_submission_),
    ...
]
```

## Запуск программы:

```
python manage.py runserver
```