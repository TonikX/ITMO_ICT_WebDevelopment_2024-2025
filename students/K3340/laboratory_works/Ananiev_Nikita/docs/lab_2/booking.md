## Приложение Bookings.
### Назначение: отвечает за логику работы с бронированиями и отзывами.
### Модели:
```python
class Booking(models.Model):
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    person_count = models.PositiveIntegerField(null=False, default=1)
    checked_in = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    add_info = models.TextField()
    client = ForeignKey(HotelBaseAccount, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(end_date__gt=models.F("start_date")), name="start_end_check")]

    def __str__(self):
        return f"Booking | from {self.start_date} to {self.end_date}| {self.client.firstname} {self.client.lastname}"


class Review(models.Model):
    date = models.DateField(auto_now_add=True)
    rate = models.IntegerField(null=False)
    description = models.TextField()
    client = models.ForeignKey(HotelBaseAccount, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(rate__lte=10), name='rate less than 10'),
                       models.CheckConstraint(condition=models.Q(rate__gte=1), name='rate more than 1')]

    def __str__(self):
        return f"Review | from {self.date} by {self.client.firstname} {self.client.lastname}"
```
### URLs:
```python
urlpatterns = [
    path('add_booking/<int:room_id>', views.CreateBookingView.as_view(), name='add_booking'),
    path('my_bookings/', views.ListBookingView.as_view(), name='my_bookings'),
    path('my_bookings/delete/<int:pk>', views.delete_booking, name='delete_booking'),
    path('my_bookings/update/<int:pk>', views.UpdateBookingView.as_view(), name='update_booking'),
]
```

### Представления:
```python
class CreateBookingView(LoginRequiredMixin, CreateView):
    model = Booking
    template_name = "add_booking.html"

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
```