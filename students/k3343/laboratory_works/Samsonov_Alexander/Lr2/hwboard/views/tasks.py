from datetime import date

from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView

from hwboard.forms import CreateAssignmentForm, EditAssignmentForm
from hwboard.models import Student, Task, Assignment


class TasksRoot(TemplateView):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context['student'] is None:
            return redirect('root')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_contents'] = 'tasks/tasks.html'
        context['title'] = 'All tasks'
        context['account'] = 'account/account_info.html'
        context['student'] = None

        user_id = self.request.session.get('user_id')

        if not user_id:
            return context

        student = Student.objects.get(pk=user_id)
        tasks = Task.objects.filter(student_classes=student.student_class).order_by('due_date')

        buffer = ()

        for task in tasks:
            try:
                assignment = Assignment.objects.get(student=student, task=task)
                if assignment.status == 'gd':
                    continue
                buffer += (task,)
            except Assignment.DoesNotExist:
                buffer += (task,)

        context['student'] = student
        context['tasks'] = buffer

        return context


class TaskIdView(DetailView):
    model = Task
    template_name = 'base.html'
    context_object_name = 'task'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()

        if context['student'] is None:
            return redirect('root')

        try:
            assignment = Assignment.objects.get(student=context['student'], task=context['task'])
            context['form'] = EditAssignmentForm()
            context['assignment_text'] = assignment
        except Assignment.DoesNotExist:
            context['form'] = CreateAssignmentForm()
            context['assignment_text'] = None

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_contents'] = 'tasks/task_details.html'
        context['title'] = 'Task'
        context['account'] = 'account/account_info.html'
        context['student'] = None

        try:
            user_id = self.request.session.get('user_id')
            student = Student.objects.get(pk=user_id)

            if student.student_class not in context['task'].student_classes.all():
                return context

            context['student'] = student
        except Student.DoesNotExist:
            pass
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        user_id = self.request.session.get('user_id')

        if not user_id:
            return redirect('/')

        try:
            assignment = Assignment.objects.get(student=context['student'], task=context['task'])
            form = EditAssignmentForm(request.POST, instance=assignment)
        except Assignment.DoesNotExist:
            form = CreateAssignmentForm(request.POST)

        if not form.is_valid():
            return self.render_to_response(self.get_context_data(form=form))

        assignment = form.save(commit=False)
        assignment.task = self.object
        assignment.student = Student.objects.get(pk=user_id)
        assignment.date_hand_in = date.today()
        assignment.status = 'pd'
        assignment.save()
        return redirect('root')
