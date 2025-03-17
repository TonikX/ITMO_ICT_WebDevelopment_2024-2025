from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView, CreateView
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import PermissionDenied

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

        search_query = self.request.GET.get('search', '')

        tasks = Task.objects.filter(student_classes=student.student_class).order_by('expire_at')
        if search_query:
            tasks = tasks.filter(Q(title__icontains=search_query))

        paginator = Paginator(tasks, 2)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        data = []
        for task in page_obj:
            data.append({
                'task': task,
                'assignment': Assignment.objects.filter(student=student, task=task).first()
            })

        context['student'] = student
        context['data'] = data
        context['page_obj'] = page_obj
        context['search_query'] = search_query

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
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Вы должны быть авторизованы как студент.")

        try:
            student = Student.objects.get(username=self.request.user.username)
            form.instance.student = student
        except Student.DoesNotExist:
            raise PermissionDenied("Пользователь не найден в базе данных студентов.")

        form.instance.received_at = timezone.now()
        form.instance.status = Statuses.PENDING

        task_id = self.kwargs.get('task_id')
        form.instance.task_id = task_id

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session.get('user_id')

        if user_id:
            try:
                student = Student.objects.get(pk=user_id)
                context['student'] = student
            except Student.DoesNotExist:
                pass

        return context