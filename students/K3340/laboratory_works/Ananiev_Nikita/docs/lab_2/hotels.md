## Приложение Hotel_app.
### Назначение: отвечает за логику работы с данными об отелях и номерах.
### Модели:
```python
class Hotel(models.Model):
    name = models.CharField(max_length=128, unique=True, null=False)
    address = models.CharField(max_length=128, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    description = models.TextField()

    @property
    def first_picture(self):
        return self.hotelpicture_set.first()

    def __str__(self):
        return f"{self.name}. Address: {self.address}"


class Room(models.Model):
    number = models.PositiveIntegerField(null=False)
    area = models.CharField(max_length=128, null=False)
    day_price = models.PositiveIntegerField(null=False)
    peculiarities = models.TextField()
    max_person_count = models.PositiveIntegerField(default=2)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=False)
    types = models.ManyToManyField('RoomType')

    @property
    def first_picture(self):
        return self.roompicture_set.first()

    def __str__(self):
        return f"Room {self.number} in the {self.hotel} hotel. Area {self.area}"


class RoomType(models.Model):
    type = models.CharField(max_length=128, unique=True, null=False)
    description = models.TextField()

    def __str__(self):
        return f"Room type: {self.type}. {self.description}"


class HotelPicture(models.Model):
    title = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    upload_date = models.DateTimeField(auto_now_add=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"Hotel picture {self.title}"


class RoomPicture(models.Model):
    title = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    upload_date = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"Room picture {self.title}"
```

### URLs:
```python
urlpatterns = [
    path('', views.MainView.as_view(), name='main_page'),
    path('hotel/<int:pk>/', views.HotelDetailView.as_view(), name="hotel_details"),
    path('hotel/<int:pk>/room/', views.RoomListView.as_view(), name="room_list"),
    path('hotel/', views.HotelListView.as_view(), name="hotel_list"),
    path('hotel/<int:pk>/room/<int:id>/', views.RoomDetailView.as_view(), name="room_details"),
    path('hotel/<int:pk>/residents/', views.ResidentsListView.as_view(), name="resident_list"),
]
```

### Представления:
```python
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
```