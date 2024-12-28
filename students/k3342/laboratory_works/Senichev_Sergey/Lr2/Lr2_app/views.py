from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, Assignment, Student
from .forms import CustomUserCreationForm, LoginForm, AssignmentForm
from datetime import date


@login_required
def account_info(request):
    student = Student.objects.get(user=request.user)
    context = {
        'student': student,
        'assignments_count': Assignment.objects.filter(student=student).count(),
        'graded_assignments': Assignment.objects.filter(student=student, status='gr').count(),
    }
    return render(request, 'homework/account/info.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(
                user=user,
                name=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('homework:task_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'homework/account/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                if user.is_superuser:
                    return redirect('homework:admin_dashboard')
                return redirect('homework:task_list')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'homework/account/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('homework:login')


@login_required
def task_list(request):
    student = Student.objects.get(user=request.user)
    tasks = Task.objects.all().order_by('-issue_date')
    assignments = Assignment.objects.filter(student=student)
    assignment_dict = {assg.task_id: assg for assg in assignments}

    context = {
        'tasks': tasks,
        'assignment_dict': assignment_dict,
    }
    return render(request, 'homework/tasks/list.html', context)


@login_required
def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
    student = Student.objects.get(user=request.user)
    assignment = Assignment.objects.filter(student=student, task=task).first()

    context = {
        'task': task,
        'assignment': assignment,
    }
    return render(request, 'homework/tasks/detail.html', context)


@login_required
def submit_task(request):
    user_assignments = Assignment.objects.filter(student__user=request.user).values_list('task_id', flat=True)
    available_tasks = Task.objects.exclude(id__in=user_assignments)

    if not available_tasks.exists():
        messages.info(request, 'No available tasks to submit.')
        return redirect('homework:task_list')

    if request.method == 'POST':
        form = AssignmentForm(request.POST, user=request.user)
        if form.is_valid():
            student = Student.objects.get(user=request.user)
            assignment = form.save(commit=False)
            assignment.student = student
            assignment.date_hand_in = date.today()
            assignment.status = 'sb'
            assignment.save()
            messages.success(request, 'Assignment submitted successfully!')
            return redirect('homework:task_list')
    else:
        form = AssignmentForm(user=request.user)
    return render(request, 'homework/tasks/submit.html', {'form': form})


@login_required
def pending_tasks(request):
    student = Student.objects.get(user=request.user)
    pending_assignments = Assignment.objects.filter(
        student=student,
        status='sb',
        grade__isnull=True
    ).select_related('task')

    return render(request, 'homework/tasks/pending.html', {
        'pending_assignments': pending_assignments
    })


@login_required
def my_grades(request):
    student = Student.objects.get(user=request.user)
    graded_assignments = Assignment.objects.filter(
        student=student,
        status='gr'
    ).select_related('task')

    return render(request, 'homework/grades/my_grades.html', {
        'graded_assignments': graded_assignments
    })


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('homework:account_info')

    students = Student.objects.all().order_by('name')
    tasks = Task.objects.all().order_by('title')

    assignments = Assignment.objects.filter(
        status='gr'
    ).select_related('task', 'student')

    grades = {}
    for assignment in assignments:
        if assignment.student_id not in grades:
            grades[assignment.student_id] = {}
        grades[assignment.student_id][assignment.task_id] = assignment.grade

    context = {
        'total_students': Student.objects.count(),
        'total_tasks': Task.objects.count(),
        'pending_assignments': Assignment.objects.filter(status='sb').count(),
        'graded_assignments': Assignment.objects.filter(status='gr').count(),
        'students': students,
        'tasks': tasks,
        'grades': grades,
    }

    return render(request, 'homework/admin/dashboard.html', context)
