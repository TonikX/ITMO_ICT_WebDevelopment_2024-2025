# Отчет по лабораторной работе №2

## Задание
**Доска домашних заданий.**
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

## Структура проекта
Проект состоит из нескольких ключевых компонентов:

- **Модели**: Определяют структуру данных.
- **Админка**: Позволяет управлять данными через интерфейс администратора.
- **Формы**: Обрабатывают ввод данных от пользователей.
- **Представления**: Логика обработки запросов и генерации ответов.
- **Шаблоны**: HTML-страницы для отображения данных пользователям.
- **URL-ы**: Определяют маршрутизацию запросов.

## Модели
В проекте определены следующие модели:

- **Assignment**: Модель для представления заданий.
- **Subject**: Модель для представления предметов.
- **HomeworkSubmission**: Модель для представления сдачи домашних заданий.

### Реализация моделей
```python
from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название предмета")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class Assignment(models.Model):
    STATUS_CHOICES = [
        (True, "Активно"),
        (False, "Завершено")
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, verbose_name="Преподаватель")
    issue_date = models.DateTimeField(verbose_name="Дата выдачи")
    due_date = models.DateTimeField(verbose_name="Дата сдачи")
    task_text = models.TextField(verbose_name="Текст задания")
    penalty_info = models.TextField(null=True, blank=True, verbose_name="Информация о штрафах")
    assignment_status = models.BooleanField(default=True, choices=STATUS_CHOICES, verbose_name="Статус задания")

    def __str__(self):
        return f"{self.subject} ({self.issue_date.strftime('%d.%m.%Y')})"

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class HomeworkSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name="Задание")
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': False}, verbose_name="Ученик")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата сдачи")
    text_submission = models.TextField(verbose_name="Ответ ученика")
    grade = models.FloatField(null=True, blank=True, verbose_name="Оценка")

    def __str__(self):
        return f"{self.student.username} → {self.assignment.subject}"

    class Meta:
        verbose_name = "Сдача домашнего задания"
        verbose_name_plural = "Сдачи домашних заданий"

```
## Админка
В админке реализованы следующие админские интерфейсы:

- **SubjectAdmin**: Управление предметами. _Этот класс определяет отображение списка предметов в админке, где выводится только название предмета._
- **AssignmentAdmin**: Управление заданиями. _Этот класс позволяет администраторам и преподавателям управлять заданиями. В списке отображаются предмет, преподаватель, даты выдачи и сдачи, а также статус задания. Реализована фильтрация по предмету, преподавателю и статусу задания. Также предусмотрена фильтрация доступных заданий для преподавателей._
- **SubjectAdmin**: Управление выполнением домашних заданий. Этот класс позволяет управлять отправленными домашними заданиями. _В списке отображаются задание, ученик, дата сдачи и оценка. Оценка может быть редактируемой прямо в списке. Реализована фильтрация по заданию и ученику. Для преподавателей доступен только их список заданий._

## Настройка ролей и разрешений

Для разграничения доступа к функционалу админки были созданы две группы пользователей: `Учителя` и `Ученики`. Группы были наделены определенными правами при создании с помощью следующего кода:

```python
def create_groups():
    teachers_group, _ = Group.objects.get_or_create(name='Учителя')
    students_group, _ = Group.objects.get_or_create(name='Ученики')

    assignment_ct = ContentType.objects.get_for_model(Assignment)
    submission_ct = ContentType.objects.get_for_model(HomeworkSubmission)

    teachers_group.permissions.set([
        Permission.objects.get(codename='add_assignment', content_type=assignment_ct),
        Permission.objects.get(codename='change_assignment', content_type=assignment_ct),
        Permission.objects.get(codename='delete_assignment', content_type=assignment_ct),
        Permission.objects.get(codename='view_assignment', content_type=assignment_ct),

        Permission.objects.get(codename='add_homeworksubmission', content_type=submission_ct),
        Permission.objects.get(codename='change_homeworksubmission', content_type=submission_ct),
        Permission.objects.get(codename='delete_homeworksubmission', content_type=submission_ct),
        Permission.objects.get(codename='view_homeworksubmission', content_type=submission_ct),
    ])
```

### Назначение прав
- **Учителя** имеют полный доступ к заданиям и отправленным работам.
- **Ученики** могут просматривать задания и отправлять выполненные работы (в коде не добавлено, но возможно расширение).

## Формы
Формы используются для обработки пользовательского ввода:

- **UserRegistrationForm**: Позволяет пользователям зарегистрироваться в системе, указывая имя, фамилию, логин, пароль и роль (учитель или ученик).
- **HomeworkSubmissionForm**: Позволяет ученикам отправлять свои домашние задания в виде текстового ответа.

### Реализация форм
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import HomeworkSubmission


class UserRegistrationForm(UserCreationForm):
    role_choices = [
        ('учитель', 'Учитель'),
        ('ученик', 'Ученик'),
    ]
    role = forms.ChoiceField(choices=role_choices)
    first_name = forms.CharField(max_length=100, label='Имя Отчество')
    last_name = forms.CharField(max_length=100, label='Фамилия')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'role']


class HomeworkSubmissionForm(forms.ModelForm):
    class Meta:
        model = HomeworkSubmission
        fields = ['text_submission']  # Поле, в котором ученик будет писать свой ответ
        widgets = {
            'text_submission': forms.Textarea(attrs={'rows': 6, 'cols': 60, 'class': 'form-control'}),
        }
```

## Представления
Представления обрабатывают запросы и возвращают соответствующие ответы:

- **register**: Обрабатывает регистрацию нового пользователя. Определяет роль пользователя (учитель или ученик) и добавляет его в соответствующую группу.
- **submit_assignment**: Позволяет ученикам отправлять выполненные домашние задания. Проверяет, чтобы учителя не могли сдавать задания.
- **AssignmentListView**: Отображает список заданий. Учитывает роль пользователя: учителя видят только свои задания, ученики – все доступные.

### Реализация представлений
```python
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .models import Assignment, HomeworkSubmission
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, HomeworkSubmissionForm


# Регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            role = form.cleaned_data['role']
            if role.lower() == 'учитель':
                user.is_staff = True
                group = Group.objects.get(name='Учителя')
            elif role.lower() == 'ученик':
                group = Group.objects.get(name='Ученики')

            user.save()
            user.groups.add(group)

            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def submit_assignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)

    # Проверяем, является ли пользователь учеником
    if request.user.is_staff:
        return redirect('assignment_list')  # Преподаватели не должны сдавать задания

    if request.method == 'POST':
        form = HomeworkSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            return redirect('assignment_list')  # Перенаправляем после успешной сдачи

    else:
        form = HomeworkSubmissionForm()

    return render(request, 'submit_assignment.html', {'form': form, 'assignment': assignment})


# Класс для отображения списка заданий с оценками
class AssignmentListView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = 'assignment_list.html'
    context_object_name = 'assignments'
    paginate_by = 2

    def get_queryset(self):
        if self.request.user.is_staff:
            return Assignment.objects.filter(assignment_status=True, teacher=self.request.user).order_by('-issue_date')
        else:
            return Assignment.objects.filter(assignment_status=True).order_by('-issue_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_teacher'] = self.request.user.groups.filter(name='Учителя').exists()
        if self.request.user.is_staff:
            # Для преподавателя выбираем только те сдачи, которые принадлежат заданиям, выданным этим преподавателем
            context['submissions'] = HomeworkSubmission.objects.filter(assignment__teacher=self.request.user)
        else:
            # Для учеников показываем все сдачи, связанные с их заданиями
            context['submissions'] = HomeworkSubmission.objects.filter(student=self.request.user)
        return context


def redirect_to_login(request):
    return redirect('login')
```

## Шаблоны
Шаблоны определяют, как данные будут отображаться пользователям. Примеры шаблонов:

- **base.html**: Базовый лэйаут с шапкой и контейнером для контента.
- **login.html**: Страница входа.
- **register.html**: Страница регистрации.
- **submit_assignment.html**: Страница сдачи задания
- **assignment_list.html**: Список домашних заданий.

## URL-ы
Маршрутизация запросов осуществляется через файл `urls.py`, который определяет, какие представления будут вызываться для различных URL-адресов.
```python
urlpatterns = [
    path('', views.redirect_to_login, name='home_redirect'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Для клиентской части
    path('register/', views.register, name='register'),
    path('assignments/', views.AssignmentListView.as_view(), name='assignment_list'),
    path('submit/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
]
```
## Вывод
Проект **"Доска домашних заданий"** предоставляет удобный интерфейс для управления домашними заданиями, их сдачи и оценки. Использование Django позволяет легко расширять функциональность и поддерживать приложение.