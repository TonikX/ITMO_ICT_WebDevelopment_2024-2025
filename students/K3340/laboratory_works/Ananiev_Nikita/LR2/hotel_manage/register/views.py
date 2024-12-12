from django.shortcuts import render, redirect
from urllib.parse import unquote
from django.utils.http import url_has_allowed_host_and_scheme
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .models import HotelBaseAccount
from .forms import *

class CreateAccount(CreateView):
    model = HotelBaseAccount
    form_class = AccountCreationForm
    template_name = "register.html"
    success_url = '/'

class AdminCreateView(CreateView):
    model = HotelBaseAccount
    form_class = AdminCreationForm
    template_name = 'register.html'
    success_url = '/'

def account_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            return HttpResponse('Invalid login form.')
        data = form.cleaned_data
        account = authenticate(email=data['email'], password=data['password'])
        if account is None or not account.is_active:
            return HttpResponse('No such account found.')
        login(request, account)
        next_url = request.session['next_url']
        del request.session['next_url']
        return redirect(next_url)
    else:
        request.session['next_url'] = get_next_url(request)
        form = LoginForm()
    return render(request, "login.html", {'form': form})


def account_logout(request):
    logout(request)
    return redirect('/')


def get_next_url(request):
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return unquote(next_url)
    if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts=[request.get_host()]):
        return '/'
    return next_url
