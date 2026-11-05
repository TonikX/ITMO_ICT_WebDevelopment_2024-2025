from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView

from .forms import *


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse('admin:index')
        return reverse('tours:available')


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('tours:available')
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tours:available')
        return render(request, 'register.html', {'form': form})


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user.html'


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileEditForm(instance=request.user)
        return render(request, 'profile.html', {'form': form})

    def post(self, request):
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
        return render(request, 'profile.html', {'form': form})


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'password_change.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        return super().form_valid(form)
