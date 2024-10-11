from django.shortcuts import render, redirect
from django.views import View

from .forms import LoginForm
from .models import Student


class RootView(View):
    def get(self, request):
        context = {
            'title': 'Home',
            'main_contents': 'root.html'
        }
        if 'user_id' in request.session:
            context['is_logged_in'] = True
            context['account'] = 'account/account_info.html'
        else:
            form = LoginForm()
            context['is_logged_in'] = False
            context['form'] = form
            context['account'] = 'account/login_form.html'

        return render(request,
                      'base.html',
                      context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                student = Student.objects.get(email=email)
                if student.check_password(password):
                    request.session['user_id'] = student.id
                    request.session['name'] = student.name
                    request.session['is_logged_in'] = True
                    return redirect('/')
                else:
                    form.add_error(None, "Invalid credentials.")
            except Student.DoesNotExist:
                form.add_error(None, "Invalid credentials.")

        return render(request, 'base.html', {
            'is_logged_in': False,
            'main_contents': 'root.html',
            'account': 'account/login_form.html',
            'form': form
        })
