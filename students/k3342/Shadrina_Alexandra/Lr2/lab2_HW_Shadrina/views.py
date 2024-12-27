from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserLoginForm, HomeworkForm, SubmissionForm, GradeSubmissionForm, \
    UserUpdateForm
from .models import Homework, Submission


# Create your views here.


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def account_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'account/account.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def is_teacher(user):
    return user.role == 'teacher'


def is_student(user):
    return user.role == 'student'


# Учитель добавляет ДЗ
@login_required
@user_passes_test(is_teacher)
def add_homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.teacher = request.user
            homework.save()
            return redirect('homework_list')
    else:
        form = HomeworkForm()

    return render(request, 'teacher/add_homework.html', {'form': form})


# Учитель редактирует ДЗ
@login_required
@user_passes_test(is_teacher)
def edit_homework(request, homework_id):
    homework = get_object_or_404(Homework, id=homework_id)
    if request.method == 'POST':
        form = HomeworkForm(request.POST, instance=homework)
        if form.is_valid():
            form.save()
            return redirect('homework_list')
    else:
        form = HomeworkForm(instance=homework)

    return render(request, 'teacher/edit_homework.html', {'form': form, 'homework': homework})


# Учитель удаляет ДЗ
@login_required
@user_passes_test(is_teacher)
def delete_homework(request, homework_id):
    homework = get_object_or_404(Homework, id=homework_id)
    if request.method == 'POST':
        homework.delete()
        return redirect('homework_list')

    return render(request, 'teacher/delete_homework.html', {'homework': homework})


# Просмотр всех ДЗ
@login_required
def homework_list(request):
    homeworks = Homework.objects.all()
    return render(request, 'student/homework_list.html', {'homeworks': homeworks})


@login_required
def submission_list(request):
    submissions = Submission.objects.filter(student=request.user)
    return render(request, 'student/submission_list.html', {'submissions': submissions})


# Студент сдает ДЗ
@login_required
@user_passes_test(is_student)
def submit_homework(request, homework_id):
    homework = get_object_or_404(Homework, id=homework_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.homework = homework
            submission.save()
            return redirect('submission_list')
    else:
        form = SubmissionForm()

    return render(request, 'student/submit_homework.html', {'form': form, 'homework': homework})


# Студент редактирует ДЗ
@login_required
@user_passes_test(is_student)
def edit_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, student=request.user)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('submission_list')
    else:
        form = SubmissionForm(instance=submission)

    return render(request, 'student/edit_submission.html', {'form': form, 'submission': submission})


# Студент удаляет ДЗ
@login_required
@user_passes_test(is_student)
def delete_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, student=request.user)

    if request.method == 'POST':
        submission.delete()
        return redirect('submission_list')

    return render(request, 'student/delete_submission.html', {'submission': submission})


@login_required
@user_passes_test(is_teacher)
def grade_table(request):
    submissions = Submission.objects.all()
    return render(request, 'teacher/grade_table.html', {'submissions': submissions})


@login_required
@user_passes_test(is_teacher)
def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('grade_table')
    else:
        form = GradeSubmissionForm(instance=submission)

    return render(request, 'teacher/grade_submission.html', {'form': form, 'submission': submission})
