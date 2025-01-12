from django.contrib.auth import login
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from project_first_app.forms import OwnerForm, CarForm, CustomUserCreationForm
from project_first_app.models import Owner, Car


def detail(request, owner_id):
    try:
        p = Owner.objects.get(pk=owner_id)
    except Owner.DoesNotExist:
        raise Http404(
            "Owner does not exist")
    return render(request, 'owner.html', {'owner': p})


def owner_list(request):
    owners = Owner.objects.all()
    return render(request, 'owner_list.html', {'owners': owners})


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


def add_owner(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owner_list')
    else:
        form = OwnerForm()
    return render(request, 'add_owner.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return redirect('create_owner')
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'register.html', {'user_form': user_form})


def create_owner(request):
    if request.method == 'POST':
        owner_form = OwnerForm(request.POST)
        if owner_form.is_valid():
            owner = owner_form.save(commit=False)
            owner.user = request.user
            owner.save()
    else:
        owner_form = OwnerForm()
    return render(request, 'create_owner.html', {'owner_form': owner_form})