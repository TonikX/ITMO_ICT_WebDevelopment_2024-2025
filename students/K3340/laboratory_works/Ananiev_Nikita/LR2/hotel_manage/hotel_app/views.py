from lib2to3.fixes.fix_input import context
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, View
from django.utils import timezone
from django.db.models import Q
from .models import Hotel, Room
from booking.forms import ReviewForm
from booking.models import Review, Booking
from register.views import get_next_url
from register.models import HotelBaseAccount

class HotelListView(ListView):
    model = Hotel
    template_name = "hotel_list.html"
    context_object_name = 'hotels'
    paginate_by = 4


class HotelDetailView(LoginRequiredMixin, DetailView):
    model = Hotel
    template_name = "hotel.html"
    context_object_name = "hotel"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_list"] = Review.objects.filter(hotel__name=self.object.name)
        # context["room_list"] = Room.objects.filter(hotel__name=self.object.name)
        context["pictures"] = self.object.hotelpicture_set.all()
        context["form"] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.instance.client = request.user
            form.instance.hotel = Hotel.objects.get(pk=kwargs['pk'])
            form.save()
            return redirect(f"/hotel/{kwargs['pk']}")
        context = self.get_context_data(**kwargs)
        errors = [form.errors[field].as_text() for field in form.errors]
        context["errors"] = errors
        return render(request, self.template_name, context)


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'room_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Room.objects.filter(hotel__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hotel"] = Hotel.objects.get(pk=self.kwargs['pk'])
        return context


class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = "room.html"
    context_object_name = "room"
    # pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("id", None)
        try:
            return Room.objects.get(pk=id_)
        except:
            raise Http404('No such room')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["types"] = self.object.types.all()
        context["available"] = True
        context["room_id"] = self.object.pk
        context["pictures"] = self.object.roompicture_set.all()
        unfinished_booking = self.object.booking_set.filter(Q(finished=False) & Q(start_date__lte=timezone.now()) & Q(end_date__gte=timezone.now()))
        if unfinished_booking:
            context["available"] = False
        return context

class ResidentsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = HotelBaseAccount
    template_name = "residents_list.html"
    permission_required = 'auth.can_see_residents_table'
    context_object_name = 'residents_bookings'
    paginate_by = 10

    def get_queryset(self):
        bookings = Booking.objects.filter(start_date__gte=datetime.datetime.today() - datetime.timedelta(days=30), room__hotel__id=self.kwargs.get("pk"))
        return bookings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MainView(View):
    def get(self, request):
        return render(request, "main.html")