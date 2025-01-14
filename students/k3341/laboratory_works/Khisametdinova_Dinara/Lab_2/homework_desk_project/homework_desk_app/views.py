from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import *
from django.views.generic import ListView, CreateView, UpdateView
from .forms import UserRegistrationForm, SubmissionForm, SubjectForm, CustomAuthenticationForm, HomeworkCreateForm, GradeSubmissionForm
from .decorators import student_required, teacher_required

class RegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('login')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        return reverse_lazy('dashboard')

class UserDashboardView(LoginRequiredMixin, ListView):
    template_name = 'dashboard.html'
    context_object_name = 'submissions'
    
    def get_queryset(self): 
        user = self.request.user

        if user.role == 'student':
            return Submission.objects.filter(student=user).select_related('homework')
        
        return Submission.objects.filter(homework__subject__teachers=user).select_related('homework', 'student')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_student'] = user.role == 'student'
        context['subjects'] = Subject.objects.filter(teachers=user) if user.role == 'teacher' else Subject.objects.all()
        return context
    
class SubmissionCreateView(LoginRequiredMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'submission.html'

    def form_valid(self, form):
        homework_id = self.kwargs['homework_id']
        homework = get_object_or_404(Homework, pk=homework_id)
        form.instance.student = self.request.user
        form.instance.homework = homework
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard')

class HomeworkListView(ListView):
    model = Homework
    template_name = 'homework_list.html'
    context_object_name = 'homeworks'
    paginate_by = 10

    def get_queryset(self):
        return Homework.objects.select_related('subject')

class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject_form.html'
    success_url = '/homeworks/'

class SubjectUpdateView(UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subject_form.html'
    success_url = '/homeworks/'

class SubmissionCreateView(CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'submission.html'

    def form_valid(self, form):
        homework_id = self.kwargs['homework_id']
        homework = get_object_or_404(Homework, pk=homework_id)
        form.instance.student = self.request.user
        form.instance.homework = homework
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('homeworks')
    
def is_admin_or_teacher(user):
    return user.is_superuser or user.role == 'teacher'

@method_decorator(user_passes_test(is_admin_or_teacher), name='dispatch')
class AdminGradeTableView(ListView):
    model = Submission
    template_name = 'grade_table.html'
    context_object_name = 'submissions'
    paginate_by = 10

    def get_queryset(self):
        queryset = Submission.objects.select_related('student', 'homework', 'homework__subject')
        class_id = self.request.GET.get('class_id')
        subject_id = self.request.GET.get('subject_id')

        if class_id:
            queryset = queryset.filter(student__student_class_id=class_id)
        else:
            queryset = queryset.filter(student__student_class__isnull=True) | queryset

        if subject_id:
            queryset = queryset.filter(homework__subject_id=subject_id)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = Class.objects.all()
        context['subjects'] = Subject.objects.all()
        context['selected_class_id'] = self.request.GET.get('class_id', '')
        context['selected_subject_id'] = self.request.GET.get('subject_id', '')
        context['is_admin'] = True
        return context

class StudentGradeTableView(LoginRequiredMixin, ListView):
    model = Submission
    template_name = 'grade_table.html'
    context_object_name = 'submissions'
    paginate_by = 10

    def get_queryset(self):
        # Фильтррр только по записям текущего пользователя
        return Submission.objects.filter(student=self.request.user).select_related('homework', 'student')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = False 
        return context
    
class HomeworkCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Homework
    form_class = HomeworkCreateForm
    template_name = 'homework_create.html'
    success_url = reverse_lazy('homeworks')

    def form_valid(self, form):
        homework = form.save(commit=False)
        homework.save()
        homework.teachers.add(self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        return self.request.user.role == 'teacher'

class SubmissionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Submission
    template_name = 'submission_list.html'
    context_object_name = 'submissions'

    def get_queryset(self):
        return Submission.objects.all()

    def test_func(self):
        return self.request.user.role == 'teacher'
    
class SubmissionGradeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Submission
    template_name = 'grade_submission.html'
    context_object_name = 'submission'
    fields = ['grade']

    def get_object(self):
        submission_id = self.kwargs.get('submission_id')
        return get_object_or_404(Submission, id=submission_id)

    def test_func(self):
        return self.request.user.role == 'teacher'

    def get_success_url(self):
        return reverse_lazy('submission_list')

class HomeworkManagementView(LoginRequiredMixin, ListView):
    model = Homework
    template_name = 'homework_list.html'
    context_object_name = 'homeworks'

    @method_decorator(teacher_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return Homework.objects.filter(subject__teachers=user)
        return Homework.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homework_form'] = HomeworkCreateForm()
        return context

@method_decorator(student_required, name='dispatch')
class StudentHomeworkListView(LoginRequiredMixin, ListView):
    model = Homework
    template_name = 'student_homework_list.html' 
    context_object_name = 'homeworks'

    def get_queryset(self):
        
        return Homework.objects.all()    
