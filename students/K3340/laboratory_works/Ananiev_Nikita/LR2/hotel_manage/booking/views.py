from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect
from register.views import get_next_url
from hotel_app.models import Room
from datetime import date

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Booking
from .forms import BookingForm


class CreateBookingView(LoginRequiredMixin, CreateView):
    model = Booking
    template_name = "add_booking.html"
    #form_class = BookingForm

    def get(self, request, *args, **kwargs):
        room = Room.objects.get(pk=kwargs['room_id'])
        request.session.setdefault("success_url", get_next_url(request))
        request.session['room_num'] = room.number
        return render(request, self.template_name, {'form': BookingForm(), 'room_num': request.session['room_num']})

    def post(self, request, *args, **kwargs):
        form = BookingForm(request.POST)
        if form.is_valid():
            start, end = form.cleaned_data['start_date'], form.cleaned_data['end_date']
            intersections = Booking.objects.filter(Q(room_id=kwargs['room_id']) & Q(start_date__lte=end) & Q(end_date__gte=start))
            if intersections.exists():
                return render(request, self.template_name,
                              {'form': BookingForm(), 'error_msg': 'Found intersections, please choose other dates',
                               'room_num': request.session['room_num']})
            form.instance.client = request.user
            form.instance.room = Room.objects.get(pk=kwargs['room_id'])
            form.save()
            next_url = request.session['success_url']
            del request.session['success_url']
            del request.session['room_num']
            return redirect(next_url)
        return render(request, self.template_name, {'form': BookingForm(), 'room_num': request.session['room_num']})


class ListBookingView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "user_bookings.html"
    context_object_name = 'bookings'
    paginate_by = 5

    def get_queryset(self):
        return self.request.user.booking_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = date.today()
        return context


class UpdateBookingView(LoginRequiredMixin, UpdateView):
    model = Booking
    template_name = "update_booking.html"
    fields = ['start_date', 'end_date', 'add_info']
    success_url = "/my_bookings/"


@login_required
@csrf_exempt
def delete_booking(request, pk):
    if request.method == 'DELETE':
        booking = Booking.objects.get(pk=pk)
        booking.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

