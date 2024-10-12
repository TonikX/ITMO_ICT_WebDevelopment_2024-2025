from django.shortcuts import redirect
from django.views.generic import ListView

from hwboard.models import Student, Assignment


class GradesPersonal(ListView):
    model = Assignment
    template_name = 'base.html'
    context_object_name = 'student'

    def get_queryset(self):
        student_id = self.request.session.get('student')
        if student_id is None:
            return redirect('root')

        try:
            return self.model.objects.filter(student__pk=student_id, grade__isnull=True).all()
        except Student.DoesNotExist or Assignment.DoesNotExist:
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Your grades',
            'main_contents': 'grades/personal_grades.html',
            'account': 'account/account_info.html',

        })
        if user_id := self.request.session.get('user_id'):
            student = Student.objects.get(pk=user_id)
            context['student'] = student
            context['account'] = 'account/account_info.html'
            context['assignments'] = Assignment.objects.filter(
                student=student
            ).all()

        else:
            context['account'] = 'account/login_form.html'
            context['student'] = None

        return context


class GradesClass(ListView):
    model = Assignment
    template_name = 'base.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        student_id = self.request.session.get('student')
        if student_id is None:
            return redirect('root')

        try:
            student = Student.objects.get(pk=student_id)
            return self.model.objects.filter(student__student_class=student.student_class, grade__isnull=True).all()
        except Student.DoesNotExist or Assignment.DoesNotExist:
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['main_contents'] = 'grades/grades_all.html'
        context['title'] = 'All grades'
        context['account'] = 'account/account_info.html'
        context['student'] = None

        if user_id := self.request.session.get('user_id'):
            student = Student.objects.get(pk=user_id)
            context['student'] = student
            context['account'] = 'account/account_info.html'
            context['assignments'] = Assignment.objects.filter(
                student__student_class=student.student_class).all()

        else:
            context['account'] = 'account/login_form.html'
            context['student'] = None

        return context
