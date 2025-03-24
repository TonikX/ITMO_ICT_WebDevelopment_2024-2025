from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .models import Assignment, HomeworkSubmission
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, HomeworkSubmissionForm


# Регистрация нового пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            role = form.cleaned_data['role']
            if role.lower() == 'учитель':
                user.is_staff = True
                group = Group.objects.get(name='Учителя')
            elif role.lower() == 'ученик':
                group = Group.objects.get(name='Ученики')

            user.save()
            user.groups.add(group)

            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def submit_assignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)

    # Проверяем, является ли пользователь учеником
    if request.user.is_staff:
        return redirect('assignment_list')  # Преподаватели не должны сдавать задания

    if request.method == 'POST':
        form = HomeworkSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            return redirect('assignment_list')  # Перенаправляем после успешной сдачи

    else:
        form = HomeworkSubmissionForm()

    return render(request, 'submit_assignment.html', {'form': form, 'assignment': assignment})


# Класс для отображения списка заданий с оценками
class AssignmentListView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = 'assignment_list.html'
    context_object_name = 'assignments'
    paginate_by = 2

    def get_queryset(self):
        if self.request.user.is_staff:
            return Assignment.objects.filter(assignment_status=True, teacher=self.request.user).order_by('-issue_date')
        else:
            return Assignment.objects.filter(assignment_status=True).order_by('-issue_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_teacher'] = self.request.user.groups.filter(name='Учителя').exists()
        if self.request.user.is_staff:
            # Для преподавателя выбираем только те сдачи, которые принадлежат заданиям, выданным этим преподавателем
            context['submissions'] = HomeworkSubmission.objects.filter(assignment__teacher=self.request.user)
        else:
            # Для учеников показываем все сдачи, связанные с их заданиями
            context['submissions'] = HomeworkSubmission.objects.filter(student=self.request.user)
        return context


def redirect_to_login(request):
    return redirect('login')
