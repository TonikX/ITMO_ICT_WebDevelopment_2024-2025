from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import Profile
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            # Создаём профиль вручную
            Profile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )
            
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')