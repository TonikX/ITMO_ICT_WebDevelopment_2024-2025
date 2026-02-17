from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Race, RaceRegistration, Comment, Car, User
from .forms import CommentForm, UserRegisterForm, CarForm
from django.contrib.auth.forms import UserCreationForm
import logging
logger = logging.getLogger(__name__)

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'racing_app/register.html'
    
    def form_valid(self, form):
        logger.info("Форма валидна, сохраняем пользователя")
        user = form.save()
        login(self.request, user)
        return redirect('home')
    
    def form_invalid(self, form):
        logger.error(f"Форма невалидна: {form.errors}")
        return self.render_to_response(self.get_context_data(form=form))

def home(request):
    races = Race.objects.all()
    return render(request, 'racing_app/race_list.html', {'races': races})

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'racing_app/register.html'
    success_url = '/login/'

class RaceListView(ListView):
    model = Race
    template_name = 'racing_app/race_list.html'
    context_object_name = 'races'
    paginate_by = 10

    def get_queryset(self):
        queryset = Race.objects.filter(is_active=True)
        
        # Фильтрация по поисковому запросу
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(location__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        return queryset

class RaceDetailView(DetailView):
    model = Race
    template_name = 'racing_app/race_detail.html'
    context_object_name = 'race'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race = self.get_object()
        
        # Регистрации на гонку с временем
        registrations = race.registrations.select_related(
            'racer', 
            'racer__car', 
            'racer__car__team'
        ).exclude(final_time__isnull=True).order_by('final_time')
        
        # Все регистрации (включая без времени)
        all_registrations = race.registrations.select_related(
            'racer', 
            'racer__car', 
            'racer__car__team'
        ).all()
        
        # Комментарии
        comments = race.comments.filter(is_approved=True).select_related('author')
        
        # Проверка, зарегистрирован ли текущий пользователь
        user_registered = False
        user_registration = None
        if self.request.user.is_authenticated:
            user_registration = RaceRegistration.objects.filter(
                race=race, 
                racer=self.request.user
            ).first()
            user_registered = user_registration is not None
        
        context.update({
            'registrations': registrations,
            'all_registrations': all_registrations,
            'comments': comments,
            'comment_form': CommentForm(),
            'user_registered': user_registered,
            'user_registration': user_registration,
        })
        return context

class RaceRegistrationCreateView(LoginRequiredMixin, CreateView):
    model = RaceRegistration
    fields = []
    template_name = 'racing_app/registration_form.html'

    def form_valid(self, form):
        race = get_object_or_404(Race, pk=self.kwargs['pk'])
        
        # Проверяем, не зарегистрирован ли уже пользователь
        if RaceRegistration.objects.filter(race=race, racer=self.request.user).exists():
            messages.error(self.request, 'Вы уже зарегистрированы на эту гонку!')
            return redirect('race_detail', pk=race.pk)
        
        form.instance.racer = self.request.user
        form.instance.race = race
        
        messages.success(self.request, 'Вы успешно зарегистрированы на гонку!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('race_detail', kwargs={'pk': self.kwargs['pk']})

class RaceRegistrationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RaceRegistration
    fields = []  # Пользователи не могут редактировать регистрацию, только админ
    template_name = 'racing_app/registration_form.html'

    def test_func(self):
        registration = self.get_object()
        return self.request.user == registration.racer

    def get_success_url(self):
        return reverse_lazy('race_detail', kwargs={'pk': self.get_object().race.pk})

class RaceRegistrationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RaceRegistration
    template_name = 'racing_app/registration_confirm_delete.html'

    def test_func(self):
        registration = self.get_object()
        return self.request.user == registration.racer

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Регистрация на гонку отменена!')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('race_detail', kwargs={'pk': self.get_object().race.pk})

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'racing_app/comment_form.html'

    def form_valid(self, form):
        race = get_object_or_404(Race, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.race = race
        
        messages.success(self.request, 'Комментарий добавлен!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('race_detail', kwargs={'pk': self.kwargs['pk']})

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'racing_app/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Регистрация прошла успешно! Теперь вы можете войти.')
        return response

@login_required
def user_registrations(request):
    registrations = RaceRegistration.objects.filter(
        racer=request.user
    ).select_related('race').order_by('-race__date')
    
    # Создаем автомобиль если его нет
    if not hasattr(request.user, 'car'):
        if request.method == 'POST':
            car_form = CarForm(request.POST)
            if car_form.is_valid():
                car = car_form.save(commit=False)
                car.owner = request.user
                car.save()
                messages.success(request, 'Информация об автомобиле добавлена!')
                return redirect('user_registrations')
        else:
            car_form = CarForm()
    else:
        car_form = None
    
    return render(request, 'racing_app/user_registrations.html', {
        'registrations': registrations,
        'car_form': car_form,
        'user_car': getattr(request.user, 'car', None),
    })