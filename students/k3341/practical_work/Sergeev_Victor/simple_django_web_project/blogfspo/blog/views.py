from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http import Http404, HttpResponse
from . import models, forms
import datetime

class CarList(ListView):
    model = models.Car
    template_name = 'templates/car_list_view.html'

class CarRetrieveView(DetailView):
    model = models.Car
    template_name = 'templates/car_detail.html'

class CarListCRUD(ListView):
    model = models.Car
    template_name = 'templates/car_list_crud.html'

class CarUpdateView(UpdateView):
    model = models.Car
    fields = ['gov_number', 'model', 'brand', 'color']
    template_name = 'templates/car_update.html'
    success_url = '/car/list/'

class CarCreateView(CreateView):
    model = models.Car
    fields = ['gov_number', 'model', 'brand', 'color']
    template_name = 'templates/car_create.html'
    success_url = '/car/list/'

class CarDeleteView(DeleteView):
    model = models.Car
    template_name = 'templates/car_delete.html'
    success_url = '/car/list'

def detail_owner(request, owner_id):
    try:
        p = models.CarOwner.objects.get(pk=owner_id)
    except models.CarOwner.DoesNotExist:
        print('lol')
        raise Http404('no such car owner')

    return render(request, 'templates/owner.html', {'owner': p})

def detail_owner_list(request):
    context = {}
    context['dataset'] = models.CarOwner.objects.all()
    return render(request, 'templates/owner_list.html', context)

def example_view(request):
    # fetch date and time
    now = datetime.datetime.now()
    # convert to string
    html = "Time is {}".format(now)
    # return response
    return HttpResponse(html)

def create_owner(request):
    context = {}
    form = forms.OwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, 'templates/create_owner.html', context)