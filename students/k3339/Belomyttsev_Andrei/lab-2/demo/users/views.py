from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .forms import LoginUserForm, RegisterUserForm

def login_user(request):
  if request.method == 'POST':
    form = LoginUserForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      user = authenticate(request, username=cd['username'], password=cd['password'])
      if user and user.is_active:
        login(request, user)
        return HttpResponseRedirect(reverse('home'))
  else:
    form = LoginUserForm()
  return render(request, 'users/login.html', {'form': form})

def logout_user(request):
  logout(request)
  return HttpResponseRedirect(reverse('users:login'))

def register(request):
  if request.method == 'POST':
    form = RegisterUserForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password'])
      user.save()
      return HttpResponseRedirect(reverse('users:login'))
  else:
    form = RegisterUserForm()
  return render(request, 'users/register.html', {'form': form})