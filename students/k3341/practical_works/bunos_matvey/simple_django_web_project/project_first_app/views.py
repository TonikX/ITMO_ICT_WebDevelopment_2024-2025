from django.shortcuts import render, get_object_or_404

from .forms import CustomUserCreationForm, CarForm
from .models import CustomUser, Car
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy


class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'


class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')


class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')


class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('car_list')


def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, 'user_detail.html', {'user': user})


def users_list(request):
    users = CustomUser.objects.all()
    return render(request, 'users_list.html', {'users': users})


class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('users_list')


class UserUpdateView(UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'passport_number', 'home_address', 'nationality']
    template_name = 'user_form.html'
    success_url = reverse_lazy('users_list')