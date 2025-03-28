from django.http import HttpResponseForbidden
from django.template.context_processors import request

from .forms import SubmissionForm
from .models import Homework, Submission, Subject, Profile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect


def submit_homework(request, homework_id):
    # homework = Homework.objects.get(id=homework_id)
    homework = get_object_or_404(Homework, id=homework_id)
    user = request.user
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Нужно войти.")

        has_submitted = Submission.objects.filter(student=user, homework=homework).exists()

        context = {'homework': homework, 'has_submitted': has_submitted}

        if has_submitted:
            # Если задание уже отправлено, перенаправить на страницу "уже отправлено"
            # return redirect('already_submitted', homework_id=homework_id)
            return render(request, 'already_submitted.html', {'homework_id': homework_id})
        else:
            # Если задание не отправлено, отобразить страницу для отправки задания
            return render(request, 'submit_homework.html', context)
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.homework = homework
            submission.student = user
            submission.save()
        return redirect('/homeworks/')


def logout_view(request):
    logout(request)
    # После выхода из системы перенаправляем на страницу входа (или другую страницу по вашему выбору)
    return redirect('login')


def homework_list(request):
    subjects = Subject.objects.all()
    homeworks = Homework.objects.all()

    selected_subject = request.GET.get('selected_subject')
    if selected_subject:
        homeworks = homeworks.filter(subject__name=selected_subject)

    return render(request, 'homework_list.html', {
        'homeworks': homeworks,
        'subjects': subjects,
        'selected_subject': selected_subject,  # Передаем выбранный предмет в шаблон
    })

def grades_table(request):
    subjects = Subject.objects.all()

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        selected_subject = get_object_or_404(Subject, pk=subject_id)
        submissions = Submission.objects.filter(homework__subject=selected_subject)
    else:
        selected_subject = subjects.first()
        submissions = Submission.objects.filter(homework__subject=selected_subject)


    return render(request, 'grades_table.html', {
        'submissions': submissions,
        'subjects': subjects,
        'selected_subject': selected_subject,  # Передаем выбранный предмет в шаблон
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_authenticated and user.username == 'Teacher' or user.username == 'home':
                return redirect('/admin/')
            else:
                return redirect('/homeworks/')
        else:
            return render(request, 'login.html', {'error_message': 'Неверные учетные данные'})

    return render(request, 'login.html')

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
