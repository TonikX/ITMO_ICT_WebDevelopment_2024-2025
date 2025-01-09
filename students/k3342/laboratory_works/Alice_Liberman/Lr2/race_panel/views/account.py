from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView

from race_panel.forms import LoginForm, RegisterRacerForm
from race_panel.models import Racer


class RacerAccountView(TemplateView):
    template_name = 'account/root.html'

    def get(self, request, *args, **kwargs):
        session_user = request.session.get('user_id', None)
        try:
            user_model = Racer.objects.get(id=session_user)

            return render(request, self.template_name, {'userinfo': user_model})
        except Racer.DoesNotExist:
            return redirect('login')


class LoginRacerView(FormView):
    template_name = "account/login.html"

    form_class = LoginForm
    success_url = reverse_lazy("root")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        try:
            user = Racer.objects.get(email=email)
        except Racer.DoesNotExist:
            form.add_error("email", "No user with this email was found.")
            return self.form_invalid(form)
        if user.check_password(password):
            self.request.session["user_id"] = user.id
            return redirect(self.success_url)
        else:
            form.add_error("password", "Incorrect password.")
            return super().form_valid(form)


class RegisterRacerView(CreateView):
    template_name = "account/register.html"
    model = Racer
    success_url = reverse_lazy("root")
    fields = ['name', 'email', 'password']

    def form_valid(self, form):
        racer = form.save(commit=False)
        racer.set_password(form.cleaned_data["password"])
        self.request.session["user_id"] = racer.id
        racer.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegisterRacerForm()
        return context


class LogoutRacerView(View):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return redirect("root")


