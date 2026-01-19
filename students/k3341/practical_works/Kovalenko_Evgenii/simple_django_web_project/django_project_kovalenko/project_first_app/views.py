from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CarOwnerUser, Car, Ownership, DrivingLicense
from .forms import CarOwnerUserCreationForm, CarOwnerUserUpdateForm, CarForm


# Функциональное представление для списка пользователей
def users_list(request):
    users = CarOwnerUser.objects.all()
    return render(request, 'users_list.html', {'users': users})


# Функциональное представление для деталей пользователя
def user_detail(request, user_id):
    try:
        user = CarOwnerUser.objects.get(pk=user_id)
        ownerships = Ownership.objects.filter(owner=user)
        licenses = DrivingLicense.objects.filter(owner=user)
    except CarOwnerUser.DoesNotExist:
        raise Http404("Пользователь не найден")

    context = {
        'user': user,
        'ownerships': ownerships,
        'licenses': licenses
    }
    return render(request, 'user_detail.html', context)


# Функциональное представление для создания пользователя
def create_user(request):
    if request.method == 'POST':
        form = CarOwnerUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users_list')
    else:
        form = CarOwnerUserCreationForm()

    return render(request, 'create_user.html', {'form': form})


# Функциональное представление для редактирования пользователя
@login_required
def update_user(request, user_id):
    user = get_object_or_404(CarOwnerUser, pk=user_id)

    # Проверяем, что пользователь редактирует свой профиль или является суперпользователем
    if request.user != user and not request.user.is_superuser:
        return HttpResponse('У вас нет прав для редактирования этого профиля', status=403)

    if request.method == 'POST':
        form = CarOwnerUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail', user_id=user.id)
    else:
        form = CarOwnerUserUpdateForm(instance=user)

    return render(request, 'update_user.html', {'form': form, 'user': user})


# Классовые представления для автомобилей
class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'

    def get_queryset(self):
        return Car.objects.all()


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ownerships'] = Ownership.objects.filter(car=self.object)
        return context


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')


class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')


class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('car_list')