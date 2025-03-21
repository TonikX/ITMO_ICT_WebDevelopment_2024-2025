from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from .models import Owner, ExampleModel, Publisher, Book, Car


def owner_detail(request, owner_id):
    owner = get_object_or_404(Owner, id=owner_id)

    return render(request, 'owner.html', {'owner': owner})


class ExampleList(ListView):
    # specify the model for list view
    model = ExampleModel
    template_name = 'cvb_list_view.html'

class CarList(ListView):
    model = Car
    template_name = 'car_list_view.html'

def list_view_owners(request):
    context = {}

    context["dataset"] = Owner.objects.all()

    return render(request, "list_view_owners.html", context)


def list_view(request):
    context = {}

    context["dataset"] = ExampleModel.objects.all()

    return render(request, "list_view.html", context)

from django.views.generic.detail import DetailView

class PublisherRetrieveView(DetailView):
  model = Publisher

class CarRetrieveView(DetailView):
  model = Car


class BookListView(ListView):
    model = Book
    queryset = model.objects.all()

    def get_queryset(self):
        publisher = self.request.GET.get('publisher')

        if publisher:

            try:
                publisher = int(publisher)
                queryset = self.queryset.filter(publisher=publisher)

            except ValueError:
                queryset = self.model.objects.none()

            return queryset

        return self.queryset


def create_view(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    form = ExampleForm(
        request.POST or None)  # создание экземпляра формы, передача в него данных из формы (из полей в браузере)
    if form.is_valid():  # проверка формы на корректность (валидация)
        form.save()
    context['form'] = form
    return render(request, "create_view.html", context)

def owner_create(request):
    # Если данные отправлены через POST, создаем форму с этими данными
    context = {}
    form = OwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, "create_view.html", context)

class PublisherUpdateView(UpdateView):
  model = Publisher
  fields = ['first_name', 'last_name', 'birthdate']
  success_url = '/publisher/list/'

class ExampleCreate(CreateView):
   # specify the model for create view
   model = ExampleModel
   template_name = 'cvb_create_view.html'
   # specify the fields to be displayed
   fields = ['title', 'description']

class PublisherCreateView(CreateView):
  model = Publisher
  fields = ['first_name', 'last_name', 'birthdate']
  success_url = '/publisher/list/'

class PublisherDeleteView(DeleteView):
  model = Publisher
  success_url = '/publisher/list/'

class CarCreateView(CreateView):
    model = Car
    fields = ['number', 'color', 'mark', 'model']  # Поля для формы
    template_name = 'car_form.html'  # Шаблон для отображения формы
    success_url = reverse_lazy('car_list')

class CarUpdateView(UpdateView):
    model = Car
    fields = ['number', 'color', 'mark', 'model']  # Поля для формы
    template_name = 'car_form.html'  # Шаблон для отображения формы
    success_url = reverse_lazy('car_list')

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'  # Шаблон для подтверждения удаления
    success_url = reverse_lazy('car_list')