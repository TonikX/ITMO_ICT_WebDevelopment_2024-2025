from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
import datetime
from .models import User, Car
from .forms import CarOwnerForm
from djangoProject import settings


def get_сar_owner_details(request, car_owner_id):
    try:
        сar_owner = settings.AUTH_USER_MODEL.objects.get(pk=car_owner_id)
    except settings.AUTH_USER_MODEL.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'сar_owner.html', {'сar_owner': сar_owner})


def create_сar_owner(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    form = CarOwnerForm(
        request.POST or None)  # создание экземпляра формы, передача в него данных из формы (из полей в браузере)
    if form.is_valid():  # проверка формы на корректность (валидация)
        form.save()
    context['form'] = form
    return render(request, "create_сar_owner.html", context)


def example_view(request):
    now = datetime.datetime.now()
    html = "Time is {}".format(now)
    return HttpResponse(html)


def get_owners(request):
    context = {"owners": settings.AUTH_USER_MODEL.objects.all()}
    return render(request, "owners.html", context)


def get_сar_owners(request):
    сar_owners = {"owners": settings.AUTH_USER_MODEL.objects.all()}
    return render(request, "car_owners.html", сar_owners)


class CarsList(ListView):
    model = Car
    context_object_name = 'cars'
    template_name = 'cars.html'


class CarRetrieveView(DetailView):
    model = Car


class CarListView(ListView):
    model = Car
    queryset = model.objects.all()

    def get_queryset(self):
        car = self.request.GET.get('car')

        if car:

            try:
                car = int(car)
                queryset = self.queryset.filter(car=car)

            except ValueError:
                queryset = self.model.objects.none()

            return queryset

        return self.queryset


class CarUpdateView(UpdateView):
    model = Car
    fields = ['state_number', 'brand', 'model', 'color']
    success_url = '/cars/'


class CarCreateView(CreateView):
    model = Car
    template_name = 'create_car.html'
    fields = ['state_number', 'brand', 'model', 'color']


class CarDeleteView(DeleteView):
    model = Car
    success_url = '/cars/'
