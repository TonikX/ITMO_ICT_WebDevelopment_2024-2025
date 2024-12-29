from django import http
from django.shortcuts import render
from django.views import generic

from project_first_app import forms, models


def owner(request: http.HttpRequest, owner_id: int) -> http.HttpResponse:
    try:
        owner_model = models.Owner.objects.get(id=owner_id)
    except models.Owner.DoesNotExist:
        raise http.Http404("Owner does not exist")
    return render(request, "owner.html", {"owner": owner_model})


def owners(request: http.HttpRequest) -> http.HttpResponse:
    context = {"owners": models.Owner.objects.all()}
    return render(request, "owners.html", context)


def create_owner(request: http.HttpRequest) -> http.HttpResponse:
    form = forms.OwnerForm(request.POST or None)

    if form.is_valid():
        form.save()

    context = {"form": form}
    return render(request, "create_owner.html", context)


class CarsListView(generic.ListView):
    model = models.Car
    context_object_name = "cars"
    template_name = "cars.html"


class CarDetailView(generic.DetailView):
    model = models.Car
    template_name = "car.html"


class CarCreateView(generic.CreateView):
    model = models.Car
    template_name = "car_create.html"
    fields = "__all__"
    success_url = "/cars/"


class CarUpdateView(generic.UpdateView):
    model = models.Car
    template_name = "car_update.html"
    fields = "__all__"
    success_url = "/cars/"


class CarDeleteView(generic.DeleteView):
    model = models.Car
    success_url = "/cars/"
    template_name = "car_delete.html"
