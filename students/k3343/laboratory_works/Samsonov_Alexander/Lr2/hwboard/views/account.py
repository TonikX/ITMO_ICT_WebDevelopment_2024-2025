from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from ..forms import RegisterStudentForm, LoginStudentForm
from ..models import Student


class RegisterStudentView(FormView):
    template_name = 'base.html'
    form_class = RegisterStudentForm
    success_url = '/'

    def form_valid(self, form):
        student = form.save(commit=False)
        student.set_password(form.cleaned_data['password'])
        student.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Register',
            'main_contents': 'account/register.html',
            'account': 'account/login_form.html',
            'form': RegisterStudentForm()
        })
        return context


class LoginStudentView(FormView):
    template_name = 'base.html'
    form_class = LoginStudentForm
    success_url = reverse_lazy('root')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        try:
            user = Student.objects.get(email=email)
        except Student.DoesNotExist:
            form.add_error('email', 'No user with this email was found.')
            return self.form_invalid(form)

        if user.check_password(password):
            self.request.session['user_id'] = user.id
            return redirect('/')
        else:
            form.add_error('password', 'Incorrect password.')
            return redirect('/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Login',
            'main_contents': 'root.html',
            'account': 'account/account_info.html',
            'form': RegisterStudentForm()
        })
        return context


class StudentView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Student',
            'main_contents': 'account/account_info.html',
        })

        if user_id := self.request.session.get('user_id'):
            context['student'] = Student.objects.get(pk=user_id)
            context['account'] = 'account/login_form.html'
        else:
            return redirect('root')

        return context


class LogoutAccountView(View):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return redirect('root')
