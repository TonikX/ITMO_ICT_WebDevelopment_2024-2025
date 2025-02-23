import datetime
import logging

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404, HttpResponseRedirect
from .forms import UserRegistrationForm, HomeworkSubmissionForm, GradeHomeworkForm
from django.contrib.auth import login, logout
from django.views.generic import ListView

from .models import User, Homework, GroupTeacher, Subject, StudyGroup, HomeworkSubmission, GradeHomework
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)


def home(request):
    if request.user.is_authenticated:
        context = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
    else:
        context = {
            'first_name': None,
            'last_name': None,
        }
    return render(request, 'home.html', context)


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/')
    return render(request, 'logout.html')


def show_homeworks(request):
    if request.user.is_authenticated:
        if request.user.role == 'student' and request.user.group:
            homeworks = Homework.objects.filter(group=request.user.group)
            submissions = {hw.id: HomeworkSubmission.objects.filter(student=request.user, homework=hw).first() for hw in
                           homeworks}
        elif request.user.role == 'teacher':
            homeworks = Homework.objects.filter(subject__teacher=request.user)
            submissions = {hw.id: HomeworkSubmission.objects.filter(homework=hw).first() for hw in homeworks}
        else:
            homeworks = Homework.objects.none()
            submissions = {}

        return render(request, 'homeworks.html', {'homeworks': homeworks, 'submissions': submissions})
    else:
        return HttpResponseRedirect('/login')


def show_all_subjects_specific_group(request):
    try:
        if request.user.role == 'student' and request.user.group:
            study_group = request.user.group
            teachers = GroupTeacher.objects.filter(group__letter=study_group.letter,
                                                   group__group_grade=study_group.group_grade).values_list('teacher',
                                                                                                           flat=True)
            subjects = Subject.objects.filter(teacher__in=teachers)
    except GroupTeacher.DoesNotExist:
        raise Http404("Group Teachers do not exist")

    return render(request, 'subjects.html', {'subjects': subjects})


class AllGroups(ListView):
    model = StudyGroup
    template_name = 'groups.html'
    context_object_name = 'groups'
    ordering = ['group_grade', 'letter']


def group_detail(request, group_id):
    try:
        group = StudyGroup.objects.get(pk=group_id)
        students = User.objects.filter(group__letter=group.letter, group__group_grade=group.group_grade).order_by(
            'first_name', 'last_name')
    except StudyGroup.DoesNotExist:
        raise Http404("Group does not exist")

    return render(request, 'group_detail.html', {'group': group, 'students': students})


@login_required
def show_grades(request):
    if request.user.role == 'teacher':
        students = User.objects.filter(role='student')
    elif request.user.role == 'student':
        students = User.objects.filter(group=request.user.group)
    else:
        return HttpResponseRedirect('/')

    subjects = Subject.objects.all()
    selected_subject_id = request.GET.get('subject')
    student_name = request.GET.get('student_name', '').strip()

    try:
        selected_subject_id = int(selected_subject_id) if selected_subject_id and selected_subject_id.isdigit() else None
    except ValueError:
        selected_subject_id = None

    grades = GradeHomework.objects.filter(submitted_homework__student__in=students)

    if selected_subject_id:
        grades = grades.filter(submitted_homework__homework__subject_id=selected_subject_id)

    if student_name:
        grades = grades.filter(
            submitted_homework__student__first_name__icontains=student_name
        ) | grades.filter(
            submitted_homework__student__last_name__icontains=student_name
        )

    paginator = Paginator(grades.distinct(), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'grades.html', {
        'students': students,
        'page_obj': page_obj,
        'subjects': subjects,
        'selected_subject_id': selected_subject_id,
        'student_name': student_name
    })


@login_required
def submit_homework(request, homework_id):
    homework = get_object_or_404(Homework, id=homework_id)
    submission = HomeworkSubmission.objects.filter(student=request.user, homework=homework).first()

    if request.method == "POST":
        form = HomeworkSubmissionForm(request.POST)
        if form.is_valid():
            if submission:
                submission.solution_text = form.cleaned_data["solution_text"]
                submission.submitted_at = datetime.datetime.now()
                submission.save()
            else:
                submission = form.save(commit=False)
                submission.homework = homework
                submission.student = request.user
                submission.submitted_at = datetime.datetime.now()
                submission.solution_text = form.cleaned_data["solution_text"]
                submission.save()
            return redirect("homeworks")

    else:
        form = HomeworkSubmissionForm(initial={"solution": submission.solution_text if submission else ""})

    return render(request, "submit_homework.html", {"form": form, "submission": submission})


@login_required
def view_submissions(request):
    if request.user.role != 'teacher':
        return redirect('home')

    submissions = HomeworkSubmission.objects.filter(
        homework__subject__teacher=request.user
    )

    for submission in submissions:
        submission.is_graded = submission.gradehomework_set.exists()

    return render(request, 'view_submissions.html', {'submissions': submissions})


@login_required
def grade_homework(request, submission_id):
    submission = get_object_or_404(HomeworkSubmission, id=submission_id)

    grade_homework = GradeHomework.objects.filter(submitted_homework=submission).first()

    if request.method == 'POST':
        form = GradeHomeworkForm(request.POST, instance=grade_homework)
        if form.is_valid():
            grade_homework = form.save(commit=False)
            grade_homework.submitted_homework = submission
            grade_homework.user = request.user
            grade_homework.save()
            return redirect('view_submissions')
    else:
        form = GradeHomeworkForm(instance=grade_homework)

    return render(request, 'grade_homework.html', {'form': form, 'submission': submission})
