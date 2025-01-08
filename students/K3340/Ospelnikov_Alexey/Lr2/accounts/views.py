from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm, SignInForm

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Укажите ваш url
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
             user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
             if user is not None:
                 login(request, user)
                 return redirect('home')
    else:
        form = SignInForm()
    return render(request, 'accounts/login.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('home')