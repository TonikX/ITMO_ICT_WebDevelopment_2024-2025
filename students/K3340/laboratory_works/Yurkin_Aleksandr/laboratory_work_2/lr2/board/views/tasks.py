from django.shortcuts import redirect
from django.views.generic import TemplateView

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
