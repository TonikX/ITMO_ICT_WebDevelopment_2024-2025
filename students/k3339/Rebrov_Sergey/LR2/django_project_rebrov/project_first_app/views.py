from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Task, Grade, SchoolUser, User, Discipline
from .forms import HomeworkSubmissionForm, SchoolUserCreationForm, TeachersSubmissionForm, TeachersCreateForm


def login_user(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('teachers-list')
        else:
            return redirect('homework-list')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if request.user.is_staff:
                return redirect('teachers-list')
            else:
                return redirect('homework-list')
    else:
        form = AuthenticationForm()

    return render(request, 'login_user.html', {'form': form})


def register_user(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('teachers-list')
        else:
            return redirect('homework-list')

    if request.method == 'POST':
        form = SchoolUserCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            user.save()

            SchoolUser.objects.create(user=user, class_id=form.cleaned_data['class_field'])

            login(request, user)

            if request.user.is_staff:
                return redirect('teachers-list')
            else:
                return redirect('homework-list')
    else:
        form = SchoolUserCreationForm()

    return render(request, 'register_user.html', {'form': form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login-user')


def homework_list(request):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login-user')

    schooluser = get_object_or_404(SchoolUser, user=request.user)

    tasks = Task.objects.select_related('discipline_id', 'class_id') \
        .filter(class_id=schooluser.class_id) \
        .exclude(grade__schooluser_id=schooluser.id)  \
        .order_by('due_date')

    return render(request, 'homework_list.html', {
        'schooluser': schooluser,
        'tasks': tasks
    })


def homework_submit(request, task_id):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login-user')

    task = get_object_or_404(Task, id=task_id)
    schooluser = get_object_or_404(SchoolUser, user=request.user)

    if task.class_id != schooluser.class_id or Grade.objects.filter(task_id=task_id, schooluser_id=schooluser.id).exists():
        return redirect('homework-list')

    if request.method == 'POST':
        form = HomeworkSubmissionForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.schooluser_id = schooluser
            grade.task_id = task
            grade.save()
            return redirect('homework-list')
    else:
        form = HomeworkSubmissionForm()

    return render(request, 'homework_submit.html', {
        'schooluser': schooluser,
        'form': form,
        'task': task
    })


def grade_table(request):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('login-user')

    current_schooluser = get_object_or_404(SchoolUser, user=request.user)
    classmates = SchoolUser.objects.filter(class_id=current_schooluser.class_id, user__is_staff=False)
    disciplines = Discipline.objects.filter(task__grade__schooluser_id__class_id=current_schooluser.class_id).distinct()

    table = []

    for schooluser in classmates:
        row = [f"{schooluser.user.first_name} {schooluser.user.last_name}"]

        for discipline in disciplines:
            schooluser_grades = Grade.objects.filter(schooluser_id=schooluser, task_id__discipline_id=discipline)

            if schooluser_grades.exists():
                row.append(', '.join([str(grade.number if grade.number is not None else 'н') for grade in schooluser_grades]))
            else:
                row.append('Нет оценок')

        table.append(row)

    return render(request, 'grade_table.html', {
        'schooluser': current_schooluser,
        'table': table,
        'disciplines': disciplines
    })


def teachers_list(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login-user')

    schooluser = get_object_or_404(SchoolUser, user=request.user)

    grades = Grade.objects.select_related('task_id').filter(
        number__isnull=True,
        task_id__teacher_id=schooluser.id
    ).order_by('task_id__due_date')

    return render(request, 'teachers_list.html', {
        'schooluser': schooluser,
        'grades': grades
    })


def teachers_submit(request, grade_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login-user')

    grade = get_object_or_404(Grade, id=grade_id)
    schooluser = get_object_or_404(SchoolUser, user=request.user)

    if grade.task_id.teacher_id.id != schooluser.id or grade.number is not None:
        return redirect('teachers-list')

    if request.method == 'POST':
        form = TeachersSubmissionForm(request.POST, instance=grade)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.save()
            return redirect('teachers-list')
    else:
        form = TeachersSubmissionForm()

    return render(request, 'teachers_submit.html', {
        'schooluser': schooluser,
        'form': form,
        'grade': grade
    })


def teachers_create(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login-user')

    schooluser = get_object_or_404(SchoolUser, user=request.user)

    if request.method == 'POST':
        form = TeachersCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.teacher_id = schooluser
            task.save()
            return redirect('teachers-list')
    else:
        form = TeachersCreateForm()

    return render(request, 'teachers_create.html', {
        'schooluser': schooluser,
        'form': form
    })
