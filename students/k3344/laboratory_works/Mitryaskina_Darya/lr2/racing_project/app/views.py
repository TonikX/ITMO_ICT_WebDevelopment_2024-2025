from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .forms import RegistrationForm, CommentForm, UserCreationForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm
from .models import Race, Registration, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

@login_required
def register_racer(request, race_id):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            race = Race.objects.get(id=race_id)
            registration.race = race
            registration.save()
            return redirect('race_list')
    else:
        form = RegistrationForm()
    return render(request, 'register_racer.html', {'form': form})


@login_required
def edit_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id)
    
    # Проверяем, что пользователь является владельцем регистрации
    if registration.user != request.user:
        return HttpResponseForbidden("Вы не можете редактировать эту регистрацию.")
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Или заменить на нужное представление
    else:
        form = RegistrationForm(instance=registration)
    
    return render(request, 'edit_registration.html', {'form': form, 'registration': registration})


@login_required
def add_comment(request, race_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            race = Race.objects.get(id=race_id)
            comment.race = race
            comment.save()
            return redirect('race_detailes', pk=race_id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})


class RaceList(ListView):
    model = Race
    template_name = 'race_list.html'
    context_object_name = 'races'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        return queryset

class ProfileList(LoginRequiredMixin, ListView):
    model = Registration
    template_name = 'registration_list.html'
    context_object_name = 'registrations'

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user)
    

class RaceDetailes(DetailView):
    model = Race
    fields = ['id', 'name', 'date', 'location', 'result']
    template_name = 'race_detailes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race = self.object
        context['comments'] = race.comments.all()
        return context
    
class DeleteRegistration(DeleteView):
    model = Registration
    template_name = 'registration_confirm_delete.html'
    success_url = '/profile'
    

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('race_list')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('race_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('race_list')  # Перенаправление на страницу после успешного входа
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('login')