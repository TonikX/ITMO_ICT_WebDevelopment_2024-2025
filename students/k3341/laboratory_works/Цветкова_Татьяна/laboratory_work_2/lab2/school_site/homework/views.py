from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Homework, Submission, Grade
from django import forms


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['text']


def homework_list(request):
    homeworks = Homework.objects.all()
    return render(request, 'homework/list.html', {'homeworks': homeworks})


@login_required
def submit_homework(request, homework_id):
    homework = get_object_or_404(Homework, id=homework_id)

    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.homework = homework
            submission.save()
            return redirect('homework_list')
    else:
        form = SubmissionForm()

    return render(request, 'homework/submit.html', {'form': form, 'homework': homework})


def grade_table(request):
    grades = Grade.objects.select_related('submission__student', 'submission__homework')
    return render(request, 'homework/grades.html', {'grades': grades})
