from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from ..forms import SignUpStudentForm, SignInStudentForm
from ..models import Student


class SignUpStudentView(FormView):
    template_name = 'signup.html'
    form_class = SignUpStudentForm
    success_url = '/'

    def form_valid(self, form):
        student = form.save(commit=False)
        student.set_password(form.cleaned_data['password'])
        student.save()

        self.request.session['user_id'] = student.id

        return super().form_valid(form)


class SignInStudentView(FormView):
    template_name = 'signin.html'
    form_class = SignInStudentForm
    success_url = reverse_lazy('root')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        try:
            user = Student.objects.get(username=username)
        except Student.DoesNotExist:
            form.add_error('username', 'Incorrect username')
            return self.form_invalid(form)

        if user.check_password(password):
            self.request.session['user_id'] = user.id
            return redirect('/')
        else:
            form.add_error('password', 'Incorrect password')
            return self.form_invalid(form)


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
