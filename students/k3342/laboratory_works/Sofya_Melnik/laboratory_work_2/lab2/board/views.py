from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, HomeworkForm, SubmissionForm, GradeSubmissionForm, UserUpdateForm
from .models import Homework, Submission


def is_teacher(user):
    return user.role == 'teacher'

def is_student(user):
    return user.role == 'student'

def main(request):
    return render(request, 'main.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('main')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def account_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'account.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def homework_list(request):
    homeworks = Homework.objects.all()
    return render(request, 'homework_list.html', {'homeworks': homeworks})

#teacher
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
    return render(request, 'add_homework.html', {'form': form})


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
    return render(request, 'edit_homework.html', {'form': form, 'homework': homework})


@login_required
@user_passes_test(is_teacher)
def delete_homework(request, homework_id):
    homework = get_object_or_404(Homework, id=homework_id)
    if request.method == 'POST':
        homework.delete()
        return redirect('homework_list')

    return render(request, 'delete_homework.html', {'homework': homework})

@login_required
@user_passes_test(is_teacher)
def submission_list(request):
    submissions = Submission.objects.all()
    return render(request, 'submission_list.html', {'submissions': submissions})

@login_required
@user_passes_test(is_teacher)
def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    form = GradeSubmissionForm(request.POST or None, instance=submission)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Оценка сохранена!")
            return redirect('submission_list')
        else:
            messages.error(request, "Некорректная оценка!")
    return render(request, 'grade_submission.html', {'form': form, 'submission': submission})

#student
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
            return redirect('student_submission_list')
    else:
        form = SubmissionForm()
    return render(request, 'submit_homework.html', {'form': form, 'homework': homework})

@login_required
@user_passes_test(is_student)
def edit_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, student=request.user)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('student_submission_list')
    else:
        form = SubmissionForm(instance=submission)
    return render(request, 'edit_submission.html', {'form': form, 'submission': submission})

@login_required
@user_passes_test(is_student)
def delete_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, student=request.user)
    if request.method == 'POST':
        submission.delete()
        return redirect('student_submission_list')
    return render(request, 'delete_submission.html', {'submission': submission})

@login_required
@user_passes_test(is_student)
def student_submission_list(request):
    submissions = Submission.objects.filter(student=request.user)
    return render(request, 'student_submission_list.html', {'submissions': submissions})

@login_required
@user_passes_test(is_student)
def student_grade_table(request):
    submissions = Submission.objects.select_related("student", "homework").only(
        "student__username", "homework__subject", "grade"
    )
    return render(request, 'student_grade_table.html', {'submissions': submissions})

