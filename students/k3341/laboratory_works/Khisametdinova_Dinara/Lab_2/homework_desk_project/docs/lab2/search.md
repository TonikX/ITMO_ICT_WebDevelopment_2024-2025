# Поиск

Система поиска позволяет пользователям находить информацию о заданиях и выполнении домашней работы в приложении, используя ключевые слова. Функциональность реализована с использованием **Bootstrap 4** и **Django**, обеспечивая удобную навигацию и взаимодействие с результатами поиска.

## Настройки приложения и конфигурация

Приложение поиска настроено в `search/apps.py`:

```
from django.apps import AppConfig

class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'
```

Затем приложение `search` добавляется в список `INSTALLED_APPS` в файле `settings.py`, что позволяет ему интегрироваться в общий проект Django.

## Реализация поиска

Класс `AdminSearchView` отвечает за обработку запросов поиска. Он использует представление `View` и шаблон `search_results.html` для отображения результатов поиска. Поиск проводится одновременно по модели `Submission` и `Homework`, чтобы обеспечить возможность находить и студентов, и описания заданий.

```
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View
from homework_desk_app.models import Homework, Submission
from django.db import models 

class AdminSearchView(View):
    template_name = 'search_results.html'

    def get(self, request, *args, **kwargs):
        context = {}
        query = request.GET.get('q')
        
        if query:
            # Поиск по студентам в Submission
            submission_results = Submission.objects.filter(
                student__username__icontains=query
            )
            
            # Поиск по описанию и предмету в Homework
            homework_results = Homework.objects.filter(
                models.Q(description__icontains=query) |
                models.Q(subject__name__icontains=query)
            )

            # Пагинация
            submission_paginator = Paginator(submission_results, 10)
            homework_paginator = Paginator(homework_results, 10)
            submission_page_number = request.GET.get('submission_page')
            homework_page_number = request.GET.get('homework_page')

            # Установка контекста для отображения результатов
            try:
                context['submission_page_obj'] = submission_paginator.page(submission_page_number)
            except PageNotAnInteger:
                context['submission_page_obj'] = submission_paginator.page(1)
            except EmptyPage:
                context['submission_page_obj'] = submission_paginator.page(submission_paginator.num_pages)

            try:
                context['homework_page_obj'] = homework_paginator.page(homework_page_number)
            except PageNotAnInteger:
                context['homework_page_obj'] = homework_paginator.page(1)
            except EmptyPage:
                context['homework_page_obj'] = homework_paginator.page(homework_paginator.num_pages)

            # Сохранение последнего запроса для работы пагинации
            context['last_question'] = f'?q={query}'

        return render(request, self.template_name, context)
```

**Основные моменты:**

*   Поиск осуществляется с помощью метода `get`, который проверяет, есть ли запрос `q`.
*   Используются `models.Q` для комбинирования условий поиска, что позволяет фильтровать результаты по имени предмета или описанию.
*   Реализована **пагинация**, обеспечивающая вывод результатов поиска на нескольких страницах. Класс `Paginator` разбивает результаты по страницам с 10 результатами на каждую.
*   Сохранение запроса (`last_question`) необходимо для корректной работы пагинации, позволяя переходить по страницам с сохранением параметров поиска.

## Интеграция с Navbar (Base.html)

Форма поиска добавляется в навбар для удобного доступа на всех страницах. В `base.html` размещена следующая форма, стилизованная с помощью Bootstrap:

```
<form action="{% url 'search:index' %}" class="form-inline my-2 my-lg-0" method="get">
    <input class="form-control mr-sm-2" type="search" placeholder="Поиск" aria-label="Поиск" name="q" value="{{ request.GET.q }}">
    <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Поиск</button>
</form>
```

Форма отправляет запрос на `{% url 'search:index' %}` методом GET, позволяя пользователям искать информацию с сохранением запроса в адресной строке. При каждом выполнении запроса форма автоматически подставляет ранее введённое значение для удобства пользователя.

## Отображение результатов в search\_results.html

Результаты поиска отображаются в `search_results.html`, используя **Bootstrap 4** для стилизации таблиц и пагинации. Пример таблицы для вывода результатов из модели `Submission`:

```
{% if submission_page_obj %}
    <h2>Результаты поиска по студентам</h2>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Ученик</th>
                <th>Текст выполнения</th>
                <th>Дата сдачи</th>
                <th>Оценка</th>
            </tr>
        </thead>
        <tbody>
            {% for submission in submission_page_obj %}
                <tr>
                    <td>{{ submission.student.username }}</td>
                    <td>{{ submission.submitted_text }}</td>
                    <td>{{ submission.submitted_at|date:"d.m.Y H:i" }}</td>
                    <td>{{ submission.grade|default:"Не оценено" }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
{% else %}
    <p>Нет результатов по запросу.</p>
{% endif %}
```

Результаты для `Homework` отображаются аналогично, и для обеих моделей активирована пагинация, что позволяет пользователям переключаться между страницами с результатами.