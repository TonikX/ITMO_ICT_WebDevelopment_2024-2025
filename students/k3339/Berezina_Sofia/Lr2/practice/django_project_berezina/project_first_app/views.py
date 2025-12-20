from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Car
from django.contrib.auth import get_user_model
from .forms import CarForm, CustomUserCreationForm
from django.contrib import messages


User = get_user_model()

def owners(request):
    owners = User.objects.all()
    return render(request, "owners.html", {'owners': owners})

def detail(request, owner_id):
    owner = get_object_or_404(User, pk=owner_id)
    return render(request, "owner.html", {'owner': owner})

def create_owner(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Владелец успешно добавлен!')
            return redirect('owners')
    else:
        form =  CustomUserCreationForm()
    
    return render(request, 'owner_form.html', {'form': form})

def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Автомобиль успешно добавлен!')
            return redirect('cars')
    else:
        form = CarForm()
    
    return render(request, 'car_create.html', {'form': form})

class CarListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'

class CarDetailView(DetailView):
    model = Car
    template_name = 'car.html'
    context_object_name = 'car'

class CarUpdateView(UpdateView):
    model = Car
    template_name = 'car_form.html'
    fields = ['number', 'brand', 'model', 'color']
    success_url = reverse_lazy('cars')
    pk_url_kwarg = 'car_id'

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = reverse_lazy('cars')
    pk_url_kwarg = 'car_id'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Автомобиль успешно удален')
        return super().delete(request, *args, **kwargs)