from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import CustomUser, Car
from .forms import CarForm, CustomUserCreationForm, CustomUserUpdateForm
from django.views import View


class OwnerListView(ListView):
    model = CustomUser
    template_name = 'blog/list_of_owners.html'
    context_object_name = 'owners'


class OwnerCreateView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'blog/create_owner.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owner-list')
        return render(request, 'blog/create_owner.html', {'form': form})


class OwnerDetailView(DetailView):
    model = CustomUser
    template_name = 'blog/owner_detail.html'
    context_object_name = 'owner'

    def get_object(self, queryset=None):
        owner_id = self.kwargs.get('pk')
        return get_object_or_404(CustomUser, pk=owner_id)


class OwnerUpdateView(View):
    def get(self, request, pk):
        owner = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserUpdateForm(instance=owner)
        return render(request, 'blog/update_owner.html', {'form': form})

    def post(self, request, pk):
        owner = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserUpdateForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            return redirect('owner-list')
        return render(request, 'blog/update_owner.html', {'form': form})

class OwnerDeleteView(View):
    def get(self, request, pk):
        owner = get_object_or_404(CustomUser, pk=pk)
        return render(request, 'blog/delete_owner.html', {'owner': owner})

    def post(self, request, pk):
        owner = get_object_or_404(CustomUser, pk=pk)
        owner.delete()
        return redirect('owner-list')


class CarListView(ListView):
    model = Car
    template_name = 'blog/list_of_cars.html'
    context_object_name = 'cars'


class CarDetailView(DetailView):
    model = Car
    template_name = 'blog/car_detail.html'
    context_object_name = 'car'


class CarCreateView(View):
    def get(self, request):
        form = CarForm()
        return render(request, 'blog/car_form.html', {'form': form})

    def post(self, request):
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car-list')
        return render(request, 'blog/car_form.html', {'form': form})


class CarUpdateView(View):
    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        form = CarForm(instance=car)
        return render(request, 'blog/car_form.html', {'form': form})

    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car-list')
        return render(request, 'blog/car_form.html', {'form': form})


class CarDeleteView(View):
    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        return render(request, 'blog/delete_car.html', {'car': car})

    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        car.delete()
        return redirect('car-list')


