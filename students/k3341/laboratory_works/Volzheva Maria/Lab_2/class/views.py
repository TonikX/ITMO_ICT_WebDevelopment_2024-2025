from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import Http404
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
import datetime
from .models import User, Subject, Homework, Submission, Class
from .forms import UserRegistrationForm, CustomAuthenticationForm, CreateSubmissionForm
from django.urls import reverse_lazy
from Lab_2 import settings
from django.contrib.auth.decorators import login_required
import re
from django.shortcuts import render, redirect, get_object_or_404


def get_welcome(request):
    return render(request, template_name='welcome.html')


class RegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration.html'
    success_url = '/login/'  # Используйте reverse_lazy для избежания проблем с URL

    def get_context_data(self, **kwargs):
        # Вызываем родительский метод, чтобы получить контекст
        context = super().get_context_data(**kwargs)
        # Добавляем классы из базы данных в контекст
        context['classes'] = Class.objects.all()
        return context


class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm
    LOGIN_REDIRECT_URL = '/home/'


@login_required
def get_home(request):
    try:
        our_user = request.user
        if our_user.role == 'student':
            all_homeworks = Homework.objects.all().filter(classes=our_user.student_class)
            submissions = Submission.objects.all().filter(student=our_user)
            # Дополнительный поиск по запросу
            grade_query = request.GET.get('grade', '')

            if grade_query:
                try:
                    grade = int(grade_query)
                    submissions = submissions.filter(grade=grade)
                except ValueError:
                    pass
            paginator = Paginator(submissions, 2)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {'our_user': our_user, 'all_homeworks': all_homeworks, 'page_obj': page_obj}
            return render(request, 'home_student.html', context)

        subjects = Subject.objects.all().filter(teachers=our_user)
        context = {'our_user': our_user, 'subjects': subjects}
        return render(request, 'home_teacher.html', context)
    except Exception as e:
        # Логгирование или обработка ошибки
        raise Http404("Страница не найдена")  # Измените на нужный вам ответ


@login_required
def get_homework(request, pk):
    try:
        our_user = request.user
        homework_info = Homework.objects.get(pk=pk)
        context = {'our_user': our_user, 'homework_info': homework_info}
        return render(request, 'homework_info.html', context)
    except Exception as e:
        raise Http404("Страница не найдена")


class HomeworkRetrieveView(DetailView):
    model = Homework


@login_required
def get_submission(request, pk):
    try:
        our_user = request.user
        submission_info = Submission.objects.get(pk=pk)
        context = {'our_user': our_user, 'submission_info': submission_info}
        return render(request, 'submission_info.html', context)
    except Exception as e:
        raise Http404("Страница не найдена")


def grades_by_subject_per_class(request):
    try:
        our_user = request.user
        if our_user.role == 'teacher':
            # Извлекаем все классы

            classes = Class.objects.prefetch_related('students')

            # Создание структуры данных для передачи в шаблон
            data = {}
            for class_instance in classes:
                data[class_instance.name] = {}

                # Получаем все домашние задания для всех предметов
                homeworks = Homework.objects.prefetch_related('submission_set', 'subject').filter(
                    classes=class_instance)

                for homework in homeworks:
                    subject_name = homework.subject.name

                    # Если ещё нет такого предмета в данных для данного класса, добавляем его
                    if subject_name not in data[class_instance.name]:
                        data[class_instance.name][subject_name] = []

                    # Добавляем информацию о сдачах к домашнему заданию
                    submissions = homework.submission_set.all()
                    for submission in submissions:
                        data[class_instance.name][subject_name].append({
                            'student': submission.student.username,
                            'description': submission.homework.description,
                            'submitted_at': submission.submitted_at,
                            'grade': submission.grade,
                        })

            return render(request, 'grades_per_class.html', {'data': data, 'our_user': request.user})
        return render(request, 'not_available.html', {'our_user': our_user})
    except Exception as e:
        # Логгирование или обработка ошибки
        raise Http404("Страница не найдена")  # Измените на нужный вам ответ


def submissions_without_grades(request):
    try:
        our_user = request.user
        if our_user.role == 'teacher':
            # Извлекаем все submission без оценок (grade = null)
            submissions = Submission.objects.filter(grade__isnull=True).select_related('homework__subject')

            # Создание структуры данных для передачи в шаблон
            data = {}
            for submission in submissions:
                subject_name = submission.homework.subject.name

                # Если ещё нет такого предмета в данных, добавляем его
                if subject_name not in data:
                    data[subject_name] = []

                data[subject_name].append(submission)

            return render(request, 'submissions_without_grades.html', {'data': data, 'our_user': request.user})
        return render(request, 'not_available.html', {'our_user': our_user})
    except Exception as e:
        # Логгирование или обработка ошибки
        raise Http404("Страница не найдена")  # Измените на нужный вам ответ





# def create_submission(request, pk):
#     homework = Homework.objects.get(pk=pk)
#     form = CreateSubmissionForm(request.POST or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.homework = homework
#         instance.student = request.user
#         instance.submitted_at = datetime.datetime.now()
#         instance.save()
#     return render(request, "create_submission.html", {'form': CreateSubmissionForm(), 'our_user': request.user})


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


def grade_submission(request, pk):
    try:
        our_user = request.user
        if our_user.role == 'teacher':
            submission = get_object_or_404(Submission, id=pk)

            if request.method == 'POST':
                # Получаем оценку из формы (предполагается, что форма отправляется методом POST)
                grade = request.POST.get('grade')
                if grade is not None:
                    # Присваиваем оценку submission и сохраняем его
                    submission.grade = grade
                    submission.save()
                    # Перенаправляем на страницу с безоценочными submissions
                    return redirect('submissions_without_grades')

            return render(request, 'grade_submission.html', {'submission': submission})
        return render(request, 'not_available.html', {'our_user': our_user})
    except Exception as e:
        # Логгирование или обработка ошибки
        raise Http404("Страница не найдена")  # Измените на нужный вам ответ


# class SubmissionCreateView(CreateView):
#     model = Submission
#     template_name = 'create_submission.html'
#     fields = ['state_number', 'brand', 'model', 'color']
#     homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     submitted_text = models.TextField()
#     submitted_at = models.DateTimeField(auto_now_add=True)
#     grade = models.IntegerField(blank=True, null=True)
#
#
# def get_homework_create_submission(request):
#     # dictionary for initial data with
#     # field names as keys
#     context = {}
#     form = HomeworkForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#     context = {'form': form}
#     return render(request, "create_сar_owner.html", context)





