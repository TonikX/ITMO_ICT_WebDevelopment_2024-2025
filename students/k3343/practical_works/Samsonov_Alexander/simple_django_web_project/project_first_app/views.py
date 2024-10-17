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
        owner = Owner.objects.get(id=id)
        return render(request, 'owner_render.html', {'owners': [owner]})
    except Exception as e:
        print(e)
        return render(request, 'owner_render.html', {'owners': []})


def owners(request):
    owners_list = Owner.objects.all()
    return render(request, 'owner_render.html', {'owners': owners_list})


class CarsListVies(ListView):
    model = Car
    queryset = model.objects.all()
    template_name = 'car_render.html'

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
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['cars'] = context['object_list']  # Rename object_list to cars
        return context


def create_owner_view(request):
    context = {}

    form = OwnerCreateForm(request.POST or None)

    if form.is_valid():
        form.save()

    context['form'] = form
    return render(request, 'create_view.html', context)


class CarCreateView(CreateView):
    model = Car
    fields = ['license_plate',
              'brand',
              'model',
              'color']

    success_url = '/first/cars/list/'
    template_name = 'create_view.html'


class CarUpdateView(UpdateView):
    model = Car
    fields = ['license_plate',
              'brand',
              'model',
              'color']

    success_url = '/first/cars/list/'
    template_name = 'create_view.html'


class CarDeleteView(DeleteView):
    model = Car
    success_url = '/first/cars/list/'
    template_name = 'delete_view.html'
