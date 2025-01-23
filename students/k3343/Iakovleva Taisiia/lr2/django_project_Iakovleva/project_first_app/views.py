from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http import Http404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.urls import reverse_lazy
from django.urls import reverse

from .models import User, Flight, Reservation, Review
from .forms import ReviewForm, ReservationForm, UserForm

def login_user(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            return login_user(request) 
    else:
        form = UserForm()
    return render(request, 'authorization/register.html', {'form': form})

# Выход пользователя
def logout_view(request):
    logout(request) 
    return redirect('login')

# Список рейсов
class FlightListView(ListView):
    model = Flight
    template_name = 'flights.html'
    context_object_name = 'flights'


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reserve_flight.html'
    success_url = reverse_lazy('reservation_list') 

    def form_valid(self, form):
        form.instance.user = self.request.user  
        form.instance.flight_id = self.kwargs['flight_id'] 
        return super().form_valid(form)
    
def reserve_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id) 
    if request.method == 'POST':
        form = ReservationForm(request.POST) 
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.flight = flight 
            reservation.user = request.user
            reservation.save()
            return redirect('reservation_list') 
    else:
        form = ReservationForm() 

    return render(request, 'reserve_flight.html', {'form': form, 'flight': flight})

class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_update.html'
    success_url = reverse_lazy('reservation_list')  

class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'reservation_delete.html'
    success_url = reverse_lazy('reservation_list') 


class ReservationListView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_list.html'
    success_url = reverse_lazy('reservation_list') 

    def form_valid(self, form):
        form.instance.user = self.request.user  # Привязываем текущего пользователя к резервированию
        return super().form_valid(form)  


class ReviewCreateView(View):
    def get(self, request, flight_id):
        flight = Flight.objects.get(id=flight_id)
        form = ReviewForm()
        return render(request, 'review_form.html', {'form': form, 'flight': flight})

    def post(self, request, flight_id):
        flight = Flight.objects.get(id=flight_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.flight = flight 
            review.user = request.user  
            review.save() 
            return redirect('review_list', flight_id=flight.id) 
        return render(request, 'review_form.html', {'form': form, 'flight': flight})
    

class ReviewListView(ListView):
    model = Review
    template_name = 'review_form.html' 
    context_object_name = 'review_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flight_id = self.kwargs['flight_id']
        flight = Flight.objects.get(id=flight_id)
        context['flight'] = flight
        return context

    def get_queryset(self):
        flight_id = self.kwargs['flight_id']
        return Review.objects.filter(flight_id=flight_id)    

