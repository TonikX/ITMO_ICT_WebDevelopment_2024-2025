from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import OwnerCreateForm
from .models import Car, Owner


# Create your views here.
def index(request):
    return render(request,
                  'first_page.html',
                  {
                      'title': 'first-app',
                  })


def owner_by_id(request, id):
    try:
        owner = Owner.objects.get(pk=id)
        return render(request, 'owner.html', {'owner': owner})
    except Exception as e:
        print(e)


def owners_list(request):
    owners = Owner.objects.all()
    return render(request, 'owners.html', {'owners': owners})


def car_by_id(request, id):
    try:
        car = Car.objects.get(pk=id)
        return render(request, 'car.html', {'car': car})
    except Exception as e:
        print(e)


def cars_list(request):
    cars = Car.objects.all()
    return render(request, 'cars.html', {'cars': cars})


class CarsListView(ListView):
    model = Car
    queryset = model.objects.all()
    template_name = 'cars.html'

    def get_queryset(self):
        car_id = self.request.GET.get('id')

        if not car_id:
            return self.queryset
        try:
            car_id = int(car_id.strip())
            queryset = self.model.objects.filter(id=car_id)
        except ValueError as e:
            queryset = self.model.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = context['object_list']
        return context


class CarCreateView(CreateView):
    model = Car
    fields = ['license_plate',
              'brand',
              'model',
              'color']

    success_url = '/cars/list/'
    template_name = 'create_view.html'


class CarUpdateView(UpdateView):
    model = Car
    fields = ['license_plate',
              'brand',
              'model',
              'color']

    success_url = '/cars/list/'
    template_name = 'create_view.html'


class CarDeleteView(DeleteView):
    model = Car
    success_url = '/first/cars/list/'
    template_name = 'delete_view.html'


class OwnersListView(ListView):
    model = Owner
    queryset = model.objects.all()
    template_name = 'owners.html'

    def get_queryset(self):
        car_id = self.request.GET.get('id')

        if not car_id:
            return self.queryset
        try:
            car_id = int(car_id.strip())
            queryset = self.model.objects.filter(id=car_id)
        except ValueError as e:
            queryset = self.model.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owners'] = context['object_list']
        return context


class OwnersCreateView(CreateView):
    model = Owner
    fields = ['name',
              'surname',
              'birth_date', ]

    success_url = '/owners/list/'
    template_name = 'create_view.html'


class OwnersUpdateView(UpdateView):
    model = Owner
    fields = ['name',
              'surname',
              'birth_date', ]

    success_url = '/owners/list/'
    template_name = 'create_view.html'


class OwnersDeleteView(DeleteView):
    model = Owner
    success_url = '/owners/list/'
    template_name = 'delete_view.html'
