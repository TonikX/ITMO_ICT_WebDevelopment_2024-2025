from django.views import View
from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from science import forms, models

def index(request):
    return redirect('conference/')

class RegisterUserView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "form": forms.RegistrationForm()
        }

        return render(request, "static/templates/user/register.html", context)

    def post(self, request: HttpRequest, *args, **kwargs):
        context = {}

        form = forms.RegistrationForm(request.POST or None)
        context["form"] = form

        if not form.is_valid():
            return render(request, "static/templates/user/register.html", context)

        email = form.cleaned_data["email"]
        is_email_occupied = models.Participant.objects.filter(email=email).exists()
        if is_email_occupied:
            context["message"] = "This email has taken"
            return render(request, "static/templates/user/register.html", context)
        
        username = form.cleaned_data["username"]
        is_username_occupied = models.Participant.objects.filter(email=email).exists()
        if is_username_occupied:
            context["message"] = "This username has taken"
            return render(request, "static/templates/user/register.html", context)

        models.User.objects.create_user(
            username=username,
            email=email,
            password=form.cleaned_data["password"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
        )

        models.Participant.objects.create(
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            email=email,
            user=models.User.objects.filter(username=username)[0]
        )

        return redirect("/login/")


class LoginUserView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "form": forms.LoginUserForm(),
        }

        return render(request, "static/templates/user/login.html", context)

    def post(self, request: HttpRequest, *args, **kwargs):
        context = {
            "title": "Авторизация",
            "action": "Войти",
        }

        form = forms.LoginUserForm(request.POST or None)
        context["form"] = form

        if not form.is_valid():
            return render(request, "static/templates/user/login.html", context)

        user = authenticate(
            request=request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )

        if user is None:
            context["message"] = "Invalid username or/and password"
            return render(request, "static/templates/user/login.html", context)

        login(request=request, user=user)
        return redirect("/conference")


class UserLogout(LogoutView):
    http_method_names = ["get", "post", "options"]

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('/login/')