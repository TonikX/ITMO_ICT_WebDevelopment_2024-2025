from django.shortcuts import render, redirect, get_object_or_404

from .forms import OwnerForm, CarForm, LicenseForm, Ownership, OwnershipForm, CustomUserCreationForm
from .models import Owner, Car, License
from django.contrib.auth import login

def home(request):
    owners = Owner.objects.all()
    return render(request, 'home.html', {'owners': owners})


def owner_detail(request, pk):
    owner = get_object_or_404(Owner, pk=pk)
    return render(request, 'owner_detail.html', {'owner': owner})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def owner_list(request):
    owners = Owner.objects.all()
    return render(request, 'owner_list.html', {'owners': owners})


def ownership_list(request):
    ownerships = Ownership.objects.all()
    return render(request, 'ownership_list.html', {'ownerships': ownerships})


def ownership_create(request):
    if request.method == 'POST':
        form = OwnershipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ownership_list')
    else:
        form = OwnershipForm()
    return render(request, 'ownership_form.html', {'form': form})


def ownership_delete(request, pk):
    ownership = get_object_or_404(Ownership, pk=pk)
    if request.method == 'POST':
        ownership.delete()
        return redirect('ownership_list')
    return render(request, 'ownership_confirm_delete.html', {'object': ownership})


def owner_create(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owner_list')
    else:
        form = OwnerForm()
    return render(request, 'owner_form.html', {'form': form})


def owner_delete(request, pk):
    owner = get_object_or_404(Owner, pk=pk)
    if request.method == 'POST':
        owner.delete()
        return redirect('owner_list')
    return render(request, 'owner_confirm_delete.html', {'object': owner})


def car_list(request):
    cars = Car.objects.all()
    return render(request, 'car_list.html', {'cars': cars})


def car_create(request, owner_id=None):
    if owner_id:
        owner = get_object_or_404(Owner, pk=owner_id)
    else:
        owner = None
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            if owner:
                car.owner = owner
            car.save()
            return redirect('owner_list')
    else:
        form = CarForm()
    return render(request, 'car_form.html', {'form': form, 'owner': owner})


def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.delete()
        return redirect('car_list')
    return render(request, 'car_confirm_delete.html', {'object': car})


def license_list(request):
    licenses = License.objects.all()
    return render(request, 'license_list.html', {'licenses': licenses})


def license_create(request, owner_id=None):
    if owner_id:
        owner = get_object_or_404(Owner, pk=owner_id)
    else:
        owner = None
    if request.method == 'POST':
        form = LicenseForm(request.POST)
        if form.is_valid():
            license = form.save(commit=False)
            if owner:
                license.owner = owner
            license.save()
            return redirect('owner_list')
    else:
        form = LicenseForm()
    return render(request, 'license_form.html', {'form': form, 'owner': owner})


def license_delete(request, pk):
    license = get_object_or_404(License, pk=pk)
    if request.method == 'POST':
        license.delete()
        return redirect('license_list')
    return render(request, 'license_confirm_delete.html', {'object': license})
