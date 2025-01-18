from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)

from .forms import CarOwnerForm, CarForm, CustomUserCreationForm
from .models import CarOwner, Car


def owner_view(request, owner_id):
    owner = get_object_or_404(CarOwner, pk=owner_id)
    context = {"owner": owner}
    return render(request, "owner.html", context)


def all_owners(request):
    owners = CarOwner.objects.all()
    context = {"owners": owners}
    return render(request, "all_owners.html", context)


def add_owner(request):
    if request.method == "POST":
        form = CarOwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("all_owners")
    else:
        form = CarOwnerForm()
    return render(request, "add_owner.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


class CarListView(ListView):
    model = Car
    template_name = "car_list.html"


class CarDetailView(DetailView):
    model = Car
    template_name = "car_detail.html"


class CarUpdateView(UpdateView):
    model = Car
    fields = ["registration_number", "brand", "model", "color"]
    template_name = "car_update.html"
    success_url = "/car_list/"


class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = "car_form.html"
    success_url = "/car_list/"


class CarUpdateFormView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = "car_form.html"


class CarDeleteView(DeleteView):
    model = Car
    template_name = "car_confirm_delete.html"
    success_url = "/car_list/"
