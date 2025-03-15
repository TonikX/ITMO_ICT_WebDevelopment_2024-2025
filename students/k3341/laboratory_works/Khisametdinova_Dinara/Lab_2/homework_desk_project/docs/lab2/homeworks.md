# Управление Домашними Заданиями (Homework Management)

В системе предусмотрены раздельные интерфейсы для отображения, добавления и проверки домашних заданий для преподавателей и студентов. Студенты видят доступные задания и могут сдавать их, а преподаватели — добавлять новые задания и проверять сданные работы.

## 1\. Просмотр Списка Домашних Заданий

Страница `homework_list.html` предоставляет список всех домашних заданий, доступных преподавателю. Преподаватель может видеть список всех заданий и фильтровать их по классу и предмету. У студентов доступен аналогичный шаблон `student_homework_list.html`, где они видят доступные задания для выполнения.

### Структура `homework_list.html` для Преподавателя:

```
{% extends 'base.html' %}
{% load bootstrap4 %}

{% block title %}Управление заданиями{% endblock %}
{% block content %}
    <h2 class="mb-4">Управление заданиями</h2>

    <a href="{% url 'homework_create' %}" class="btn btn-success mb-4">Добавить новое задание</a>

    {% if homeworks %}
        <div class="list-group">
            {% for homework in homeworks %}
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">{{ homework.subject.name }}</h5>
                        <p class="card-text">{{ homework.description }}</p>
                        <p><strong>Преподаватели:</strong> {{ homework.subject.teachers.all|join:", " }}</p>
                        <a href="{% url 'submission_list' homework.id %}" class="btn btn-primary">Проверить выполнение</a>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <p>Нет доступных домашних заданий.</p>
    {% endif %}
{% endblock %}
```

### Функциональные различия для преподавателя и студента

*   **Преподаватель:** Может видеть кнопки для добавления нового задания и проверки выполнения сданных работ.
*   **Студент:** В `student_homework_list.html` отображаются задания с возможностью перехода на страницу сдачи, но без доступа к управлению заданиями.

## 2\. Форма Добавления Домашнего Задания

Преподаватель может добавить новое домашнее задание, заполнив форму на странице `homework_create.html`. Она доступна по URL `/homeworks/create/` и управляется представлением `HomeworkCreateView`. Эта форма заполняет основные поля задания, такие как предмет, дата выдачи, срок выполнения, описание и информация о штрафах.

### Код Форма `HomeworkCreateForm`:

```
class HomeworkCreateForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'issued_date', 'due_period', 'description', 'penalties_info']
        widgets = {
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
            'due_period': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'penalties_info': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(teachers=user)
```

### Особенности Фильтрации по Преподавателю

Фильтрация списка предметов выполняется в конструкторе, ограничивая выбор предметов, которые ведет текущий преподаватель. Это позволяет преподавателям назначать задания только по их собственным предметам.

## 3\. Управление Заданиями: Представления `HomeworkManagementView` и `StudentHomeworkListView`

Классы `HomeworkManagementView` и `StudentHomeworkListView` обеспечивают функциональное разделение между преподавателями и студентами:

### Код Представления `HomeworkManagementView` для Преподавателя:

```
class HomeworkManagementView(LoginRequiredMixin, ListView):
    model = Homework
    template_name = 'homework_list.html'
    context_object_name = 'homeworks'

    @method_decorator(teacher_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return Homework.objects.filter(subject__teachers=user)
        return Homework.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homework_form'] = HomeworkCreateForm()
        return context
```

### Миксины и Декораторы

Для ограничения доступа используются следующие декораторы и миксины:

*   `LoginRequiredMixin`: Убедитесь, что пользователь авторизован.
*   `teacher_required`: Проверяет, что пользователь — преподаватель. Если это не так, студент перенаправляется к своему списку заданий.

### Код Представления `StudentHomeworkListView` для Студента:

```
@method_decorator(student_required, name='dispatch')
class StudentHomeworkListView(LoginRequiredMixin, ListView):
    model = Homework
    template_name = 'student_homework_list.html' 
    context_object_name = 'homeworks'

    def get_queryset(self):
        # Студенты видят все доступные дз
        return Homework.objects.all()    
```

#### Декоратор `student_required`

Декоратор `student_required` позволяет проверять, что роль пользователя — `student`, и перенаправлять преподавателей к управлению заданиями, если они попытаются получить доступ к списку домашних заданий студентов.

## 4\. Взаимодействие с Другими Ссылками

*   **Список домашних заданий для преподавателей:** `/homeworks/`
*   **Список домашних заданий для студентов:** `/student/homeworks/`
*   **Добавление нового задания:** `/homeworks/create/`