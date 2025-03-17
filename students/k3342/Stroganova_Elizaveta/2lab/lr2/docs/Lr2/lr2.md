# ЛАБОРАТОРНАЯ РАБОТА №2

# РЕАЛИЗАЦИЯ ПРОСТОГО САЙТА СРЕДСТВАМИ DJANGO

## Цель:

Овладеть практическими навыками и умениями реализации web-сервисов
средствами Django 2.2.

## Описание

Реализовать сайт используя фреймворк Django 3 и СУБД PostgreSQL *, в
соответствии с вариантом задания лабораторной работы.


## Доска домашних заданий.

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


## Модели

```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from lr2.settings import Statuses
import hashlib
import datetime


class Class(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Student(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=256)
    name = models.CharField(max_length=40)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        hashed_password = hashlib.sha256(raw_password.encode('utf-8')).hexdigest()
        self.password = hashed_password

    def check_password(self, raw_password):
        return hashlib.sha256(raw_password.encode('utf-8')).hexdigest() == self.password


class Task(models.Model):
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateField()
    expire_at = models.DateField()
    author = models.CharField(max_length=100)
    student_classes = models.ManyToManyField(Class)

    def __str__(self):
        return self.title

    @property
    def is_past_due(self):
        return datetime.date.today() > self.expire_at


class Assignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    text = models.TextField()
    grade = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ], null=True, blank=True)
    graded_at = models.DateField(null=True, blank=True)
    received_at = models.DateField()

    status = models.IntegerField(validators=[
        MinValueValidator(min(Statuses)),
        MaxValueValidator(max(Statuses)),
    ], default=1)

    class Meta:
        unique_together = ('task', 'student')

    def __str__(self):
        return f'{self.student.name}: {self.task.title}'

```

### Эндпоинты

```python
urlpatterns = [
    path('', MainView.as_view(), name='root'),
    path('signup/', SignUpStudentView.as_view(), name='signup'),
    path('signin/', SignInStudentView.as_view(), name='signin'),
    path('logout/', LogoutAccountView.as_view(), name='logout'),
    path('tasks/', TasksView.as_view(), name='tasks_list'),
    path('tasks/<int:pk>', TaskDetailView.as_view(), name='task_details'),
    path('tasks/<int:task_id>/create_assignment', AssignmentCreateView.as_view(), name='create_assignment'),
    path('grades', GradesTableView.as_view(), name='grades_table')
]
```
### Контроллеры Views
#### Grades.py
```python
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView, CreateView
from django.utils import timezone

from ..models import Student, Task, Assignment
from lr2.settings import Statuses


class GradesTableView(TemplateView):
    template_name = 'grades.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.request.session.get('user_id')

        if not user_id:
            return context

        student = Student.objects.get(pk=user_id)
        student_class = student.student_class
        students = Student.objects.filter(student_class=student_class)
        tasks = Task.objects.filter(student_classes=student_class).order_by('expire_at')

        data = []

        for student in students:
            row = {
                'student': student,
                'assignments': []
            }
            for task in tasks:
                row['assignments'].append(Assignment.objects.filter(student=student, task=task).first())
            data.append(row)

        context['student'] = student
        context['tasks'] = tasks
        context['data'] = data

        return context

```

#### main.py
```python
from django.views.generic import TemplateView

from ..forms import SignInStudentForm
from ..models import Student


class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if user_id := self.request.session.get('user_id'):
            context['student'] = Student.objects.get(pk=user_id)

        return context

```

#### students.py
```python
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from ..forms import SignUpStudentForm, SignInStudentForm
from ..models import Student


class SignUpStudentView(FormView):
    template_name = 'signup.html'
    form_class = SignUpStudentForm
    success_url = '/'

    def form_valid(self, form):
        student = form.save(commit=False)
        student.set_password(form.cleaned_data['password'])
        student.save()

        self.request.session['user_id'] = student.id

        return super().form_valid(form)


class SignInStudentView(FormView):
    template_name = 'signin.html'
    form_class = SignInStudentForm
    success_url = reverse_lazy('root')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        try:
            user = Student.objects.get(username=username)
        except Student.DoesNotExist:
            form.add_error('username', 'Incorrect username')
            return self.form_invalid(form)

        if user.check_password(password):
            self.request.session['user_id'] = user.id
            return redirect('/')
        else:
            form.add_error('password', 'Incorrect password')
            return self.form_invalid(form)


class StudentView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Student',
            'main_contents': 'account/account_info.html',
        })

        if user_id := self.request.session.get('user_id'):
            context['student'] = Student.objects.get(pk=user_id)
            context['account'] = 'account/login_form.html'
        else:
            return redirect('root')

        return context


class LogoutAccountView(View):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return redirect('root')


```
#### tasks.py
```python
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView, CreateView
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from ..models import Student, Task, Assignment
from lr2.settings import Statuses


class TasksView(TemplateView):
    template_name = 'tasks.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context['student'] is None:
            return redirect('root')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session.get('user_id')

        if not user_id:
            return context

        student = Student.objects.get(pk=user_id)

        search_query = self.request.GET.get('search', '')

        tasks = Task.objects.filter(student_classes=student.student_class).order_by('expire_at')
        if search_query:
            tasks = tasks.filter(Q(title__icontains=search_query))

        paginator = Paginator(tasks, 2)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        data = []
        for task in page_obj:
            data.append({
                'task': task,
                'assignment': Assignment.objects.filter(student=student, task=task).first()
            })

        context['student'] = student
        context['data'] = data
        context['page_obj'] = page_obj
        context['search_query'] = search_query

        return context

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task'


class AssignmentCreateView(CreateView):
    model = Assignment
    fields = ['text']
    template_name = 'assignment_form.html'
    success_url = '/tasks'

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Вы должны быть авторизованы как студент.")

        try:
            student = Student.objects.get(username=self.request.user.username)
            form.instance.student = student
        except Student.DoesNotExist:
            raise PermissionDenied("Пользователь не найден в базе данных студентов.")

        form.instance.received_at = timezone.now()
        form.instance.status = Statuses.PENDING

        task_id = self.kwargs.get('task_id')
        form.instance.task_id = task_id

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session.get('user_id')

        if user_id:
            try:
                student = Student.objects.get(pk=user_id)
                context['student'] = student
            except Student.DoesNotExist:
                pass

        return context


```

## Формы
```python
from django import forms
from .models import Student, Assignment

class SignUpStudentForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Введите пароль'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Подтвердите пароль'
        })
    )

    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Введите ваше имя'
        })
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Введите имя пользователя'
        })
    )

    class Meta:
        model = Student
        fields = [
            'name',
            'username',
            'password',
        ]

    def clean(self):
        cleaned = super().clean()
        original_password = cleaned.get("password")
        confirm_password = cleaned.get("confirm_password")

        if original_password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned


class SignInStudentForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Введите имя пользователя'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Введите пароль'
        })
    )



class CreateAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['text']
        

```