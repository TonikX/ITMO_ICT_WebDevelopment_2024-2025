from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Hotel, Room, Booking, Review
from .forms import RegistrationForm, LoginForm, BookingForm, ReviewForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from datetime import timedelta
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class HomeView(TemplateView):
    template_name = 'home.html'


class UserRegistrationView(TemplateView):
    template_name = 'register.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
               login(request, user)
               messages.success(request, 'Вы успешно вошли!')
               return redirect('home')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Вы успешно вышли!')
        return HttpResponseRedirect(reverse_lazy('home'))


class HotelListView(ListView):
    model = Hotel
    template_name = 'hotel_list.html'
    context_object_name = 'hotels'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hotels = self.get_queryset()
        paginator = Paginator(hotels, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            hotels_page = paginator.page(page)
        except PageNotAnInteger:
            hotels_page = paginator.page(1)
        except EmptyPage:
            hotels_page = paginator.page(paginator.num_pages)

        context['hotels'] = hotels_page
        return context


class RoomListView(ListView):
    model = Room
    template_name = 'room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        return Room.objects.filter(hotel_id=hotel_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = get_object_or_404(Hotel, pk=self.kwargs.get('hotel_id'))
        return context


class RoomDetailView(DetailView):
    model = Room
    template_name = 'room_detail.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking_form'] = BookingForm()
        context['review_form'] = ReviewForm()
        context['bookings'] = Booking.objects.filter(room=self.object, user=self.request.user)
        context['reviews'] = Review.objects.filter(room=self.object)
        return context


class BookingCreateView(LoginRequiredMixin, View):
    def post(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id)
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user
            booking.save()
            messages.success(request, 'Бронирование успешно сохранено!')
            return redirect(reverse_lazy('room_detail', kwargs={'pk': room_id}))
        return render(request, 'room_detail.html', {'room': room, 'booking_form': form})


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking_update.html'
    context_object_name = 'booking'

    def get_success_url(self):
        return reverse_lazy('room_detail', kwargs={'pk': self.object.room.id})

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'booking_delete.html'
    context_object_name = 'booking'

    def get_success_url(self):
       return reverse_lazy('room_detail', kwargs={'pk': self.object.room.id})

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-check_in_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = get_object_or_404(Room, pk=self.kwargs['room_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('room_detail', kwargs={'pk': self.kwargs['room_id']})

    def form_valid(self, form):
        review = form.save(commit=False)
        review.user = self.request.user
        review.room = get_object_or_404(Room, pk=self.kwargs['room_id'])
        review.save()
        messages.success(self.request, 'Отзыв успешно добавлен!')
        return super().form_valid(form)


class MonthlyGuestListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'monthly_guests.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        today = timezone.now().date()
        last_month = today - timedelta(days=30)
        return Booking.objects.filter(check_in_date__gte=last_month).order_by('-check_in_date')