from users.models import User
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from users.forms import UserLoginForm, UserRegistrationForm
from django.contrib import auth


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('Index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)

@csrf_protect
def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Проверяем, выбрал ли пользователь "Вы турагент?"
            if form.cleaned_data.get('is_agent'):
                user.is_staff = True
                user.is_superuser = True
            user.save()
            print(f"Пользователь {user.username} успешно зарегистрирован.")
            return HttpResponseRedirect(reverse('users:login'))
        else:
            print("Ошибки формы:", form.errors)
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('Index'))