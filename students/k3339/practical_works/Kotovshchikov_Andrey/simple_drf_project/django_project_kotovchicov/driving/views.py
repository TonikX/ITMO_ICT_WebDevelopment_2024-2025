from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpRequest

from driving.models import Car, CarOwner
from driving.forms import CarForm, CarOwnerForm
from django.contrib.auth import get_user_model


def car_owner_view(request: HttpRequest, *args, **kwargs):
    context = dict()
    context["owner"] = get_object_or_404(
        CarOwner.objects.select_related("user"),
        pk=kwargs["owner_pk"],
    )

    return render(request, "driving/owner.html", context)


def car_owner_list_view(request: HttpRequest, *args, **kwargs):
    context = dict()
    context["owner_list"] = CarOwner.objects.all()
    return render(request, "driving/owner-list.html", context)


def car_owner_create_view(request: HttpRequest, *args, **kwargs):
    context = dict()
    form = CarOwnerForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data["email"]
        passport_number = form.cleaned_data["passport_number"]
        home_address = form.cleaned_data["home_address"]
        nationality = form.cleaned_data["nationality"]

        car_owner = form.save(commit=False)
        user = get_user_model().objects.create(
            email=email,
            passport_number=passport_number,
            home_address=home_address,
            nationality=nationality,
        )

        car_owner.user = user
        car_owner.save()

    context["form"] = form
    return render(request, "driving/owner-create.html", context)


class CarListView(generic.ListView):
    model = Car
    template_name = "driving/car-list.html"


class CarCreateView(generic.CreateView):
    model = Car
    form_class = CarForm
    template_name = "driving/car-create.html"
    success_url = reverse_lazy("car-list")


class CarDetailView(generic.DeleteView):
    model = Car
    template_name = "driving/car.html"
    pk_url_kwarg = "car_pk"


class CarUpdateView(generic.UpdateView):
    model = Car
    template_name = "driving/car-update.html"
    pk_url_kwarg = "car_pk"
    fields = ("state_number", "color")

    def get_success_url(self) -> str:
        return reverse_lazy("car", kwargs={"car_pk": self.object.pk})


class CarDeleteView(generic.DeleteView):
    model = Car
    success_url = reverse_lazy("car-list")
    template_name = "driving/car-delete-confirm.html"
    pk_url_kwarg = "car_pk"
