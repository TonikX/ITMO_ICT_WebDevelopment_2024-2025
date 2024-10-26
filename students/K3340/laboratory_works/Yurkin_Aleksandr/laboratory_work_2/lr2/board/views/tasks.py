from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView, CreateView
from django.utils import timezone

from ..models import Student, Task, Assignment
from lr2.settings import Statuses

class TasksView(TemplateView):
    template_name = 'tasks.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context['student'] is None:
            return redirect('root')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.request.session.get('user_id')

        if not user_id:
            return context

        student = Student.objects.get(pk=user_id)
        tasks = Task.objects.filter(student_classes=student.student_class).order_by('expire_at')

        data = []

        for task in tasks:
            data.append({
                'task': task,
                'assignment': Assignment.objects.filter(student=student, task=task).first()
            })


        context['student'] = student
        context['data'] = data

        return context

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task'


class AssignmentCreateView(CreateView):
    model = Assignment
    fields = ['text']
    template_name = 'assignment_form.html'
    success_url = '/tasks'

    def form_valid(self, form):
        form.instance.student_id = self.request.user.id
        form.instance.received_at = timezone.now()
        form.instance.status = Statuses.PENDING

        task_id = self.kwargs.get('task_id')
        form.instance.task_id = task_id

        return super().form_valid(form)
