from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView, CreateView
from django.utils import timezone

from ..models import Student, Task, Assignment
from lr2.settings import Statuses


class GradesTableView(TemplateView):
    template_name = 'grades.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.request.session.get('user_id')

        if not user_id:
            return context

        student = Student.objects.get(pk=user_id)
        student_class = student.student_class
        students = Student.objects.filter(student_class=student_class)
        tasks = Task.objects.filter(student_classes=student_class).order_by('expire_at')

        data = []

        for student in students:
            row = {
                'student': student,
                'assignments': []
            }
            for task in tasks:
                row['assignments'].append(Assignment.objects.filter(student=student, task=task).first())
            data.append(row)

        context['student'] = student
        context['tasks'] = tasks
        context['data'] = data

        return context
