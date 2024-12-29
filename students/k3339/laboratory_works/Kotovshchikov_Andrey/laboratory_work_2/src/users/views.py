from django import views
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import SignInForm, SignUpForm
from users.models import User


class SignUpView(views.View):
    def get(self, request, *args, **kwargs):
        context = {
            "title": "Регистрация",
            "form": SignUpForm(),
            "action": "Зарегистрироваться",
        }

        return render(request, "users/auth-form.html", context)

    def post(self, request: HttpRequest, *args, **kwargs):
        context = {
            "title": "Регистрация",
            "action": "Зарегистрироваться",
        }

        form = SignUpForm(request.POST or None)
        context["form"] = form

        if not form.is_valid():
            return render(request, "users/auth-form.html", context)

        email = form.cleaned_data["email"]
        is_email_occupied = User.objects.filter(email=email).exists()
        if is_email_occupied:
            context["message"] = "Email занят другим пользователем"
            return render(request, "users/auth-form.html", context)

        User.objects.create_user(
            email=email,
            password=form.cleaned_data["password"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
        )

        return redirect(reverse("sign-in"))


class SignInView(views.View):
    def get(self, request, *args, **kwargs):
        context = {
            "title": "Авторизация",
            "form": SignInForm(),
            "action": "Войти",
        }

        return render(request, "users/auth-form.html", context)

    def post(self, request: HttpRequest, *args, **kwargs):
        context = {
            "title": "Авторизация",
            "action": "Войти",
        }

        form = SignInForm(request.POST or None)
        context["form"] = form

        if not form.is_valid():
            return render(request, "users/auth-form.html", context)

        user = authenticate(
            request=request,
            username=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )

        if user is None:
            context["message"] = "Неверный логин или пароль"
            return render(request, "users/auth-form.html", context)

        login(request=request, user=user)
        return redirect(reverse("conference-list"))


@login_required
def sign_out(request: HttpRequest):
    logout(request)
    return redirect(reverse("sign-in"))
