from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)
from .models import Car
from .forms import CarOwnerForm


def owner(request, owner_id):
    User = get_user_model()
    try:
        owner = User.objects.get(pk=owner_id)
    except User.DoesNotExist:
        raise Http404("Car owner does not exist")
    return render(request, "project_first_app/owner.html", {"owner": owner})


def owner_list(request):
    User = get_user_model()
    owners = User.objects.all()
    return render(request, "project_first_app/owner_list.html", {"owners": owners})


class CarListView(ListView):
    model = Car
    context_object_name = "cars"


class CarDetailView(DetailView):
    model = Car
    context_object_name = "car"


def create_owner(request):
    context = {}
    form = CarOwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("/owners/")
    context["form"] = form
    return render(request, "project_first_app/create_owner.html", context)


class CarUpdateView(UpdateView):
    model = Car
    fields = ["car_number", "brand", "model", "color"]
    success_url = "/cars/"


class CarCreateView(CreateView):
    model = Car
    fields = ["car_number", "brand", "model", "color"]
    success_url = "/cars/"


class CarDeleteView(DeleteView):
    model = Car
    success_url = "/cars/"
