from django.shortcuts import render, redirect
from .forms import RegistrationForm, SubmissionForm
from .models import Homework, Submission

def is_teacher(user):
    return user.role == 'teacher'

def is_student(user):
    return user.role == 'student'

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def homework_list(request):
    query = request.GET.get('search', '')
    homeworks = Homework.objects.all()
    if query:
        homeworks = homeworks.filter(
            subject__icontains=query
        ) | homeworks.filter(
            description__icontains=query
        ) | homeworks.filter(
            teacher__username__icontains=query
        )

    return render(request, 'homework_list.html', {'homeworks': homeworks})

def success_view(request):
       return render(request, 'success.html')

def wrong_role_view(request):
       return render(request, 'wrong_role.html')

def submit_hw(request, hw_id):
    if is_teacher(request.user):
        return wrong_role_view(request)

    if is_student(request.user):
        hw = Homework.objects.get(pk=hw_id)

        if request.method == 'POST':
            form = SubmissionForm(request.POST)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.hw = hw
                submission.student = request.user
                submission.save()
                return success_view(request)
        else:
            form = SubmissionForm()

        return render(request, 'submit_hw.html', {'form': form, 'hw': hw})

def submissions_list(request):
    current_user = request.user

    query = request.GET.get('search', '')
    grade_query = request.GET.get('grade', '')

    submissions = Submission.objects.filter(student=current_user)

    if query:
        submissions = submissions.filter(
            hw__subject__icontains=query
        ) | submissions.filter(
            submission_text__icontains=query
        )

    if grade_query:
        try:
            grade = int(grade_query)
            submissions = submissions.filter(grade=grade)
        except ValueError:
            pass

    paginator = Paginator(submissions, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'submissions_list.html', {'page_obj': page_obj, 'request': request})