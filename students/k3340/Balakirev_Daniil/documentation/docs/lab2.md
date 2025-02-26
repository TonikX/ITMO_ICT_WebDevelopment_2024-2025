# Лабораторная работа 2

## Список отелей
### Необходимо учитывать название отеля, владельца отеля, адрес, описание, типы номеров, стоимость, вместимость, удобства.
### Необходимо реализовать следующий функционал:
Регистрация новых пользователей.

Просмотр и резервирование номеров. 

Пользователь должен иметь возможность редактирования и удаления своих резервирований.

Написание отзывов к номерам. При добавлении комментариев, должны сохраняться период проживания, текст комментария, рейтинг (1-10), информация о комментаторе.

Администратор должен иметь возможность заселить пользователя в отель и выселить из отеля средствами Django-admin.

В клиентской части должна формироваться таблица, отображающая постояльцев отеля за последний месяц.

## Модели

    class User(AbstractUser):
        pass
    
    class Hotel(models.Model):
        name = models.CharField(max_length=100)
        owner = models.CharField(max_length=100)
        address = models.CharField(max_length=100)
        description = models.TextField()
    
    
    class RoomType(models.Model):
        name = models.CharField(max_length=100)
    
    
    class Room(models.Model):
        hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
        room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        capacity = models.IntegerField()
        amenities = models.TextField()
    
    
    class Booking(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        room = models.ForeignKey(Room, on_delete=models.CASCADE)
        check_in_date = models.DateField()
        check_out_date = models.DateField()
    
    
    class Review(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
        room = models.ForeignKey(Room, on_delete=models.CASCADE)
        start_date = models.DateField()
        end_date = models.DateField()
        text = models.TextField()
        rating = models.IntegerField()


## Представления

### UserRegistrationView

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

### LoginView

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

### LogoutView

    class LogoutView(View):
        def get(self, request):
            logout(request)
            messages.success(request, 'Вы успешно вышли!')
            return HttpResponseRedirect(reverse_lazy('home'))

### HotelListView

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

### RoomListView

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

### RoomDetailView

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

### BookingCreateView

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

### BookingUpdateView

    class BookingUpdateView(LoginRequiredMixin, UpdateView):
        model = Booking
        form_class = BookingForm
        template_name = 'booking_update.html'
        context_object_name = 'booking'
    
        def get_success_url(self):
            return reverse_lazy('room_detail', kwargs={'pk': self.object.room.id})
    
        def get_queryset(self):
            return Booking.objects.filter(user=self.request.user)

### BookingDeleteView

    class BookingDeleteView(LoginRequiredMixin, DeleteView):
        model = Booking
        template_name = 'booking_delete.html'
        context_object_name = 'booking'
    
        def get_success_url(self):
           return reverse_lazy('room_detail', kwargs={'pk': self.object.room.id})
    
        def get_queryset(self):
            return Booking.objects.filter(user=self.request.user)

### BookingListView

    class BookingListView(LoginRequiredMixin, ListView):
        model = Booking
        template_name = 'booking_list.html'
        context_object_name = 'bookings'
    
        def get_queryset(self):
            return Booking.objects.filter(user=self.request.user).order_by('-check_in_date')
    
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

### ReviewCreateView

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

### MonthlyGuestListView    

    class MonthlyGuestListView(LoginRequiredMixin, ListView):
        model = Booking
        template_name = 'monthly_guests.html'
        context_object_name = 'bookings'
    
        def get_queryset(self):
            today = timezone.now().date()
            last_month = today - timedelta(days=30)
            return Booking.objects.filter(check_in_date__gte=last_month).order_by('-check_in_date')

## Пути

    urlpatterns = [
        path('', views.HomeView.as_view(), name='home'),
        path('register/', views.UserRegistrationView.as_view(), name='register'),
        path('login/', views.LoginView.as_view(), name='login'),
        path('logout/', views.LogoutView.as_view(), name='logout'),
        path('hotels/', views.HotelListView.as_view(), name='hotel_list'),
        path('hotel/<int:hotel_id>/rooms/', views.RoomListView.as_view(), name='room_list'),
        path('room/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
        path('room/<int:room_id>/booking/', views.BookingCreateView.as_view(), name='booking_create'),
        path('booking/<int:pk>/update/', views.BookingUpdateView.as_view(), name='booking_update'),
        path('booking/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),
        path('room/<int:room_id>/review/', views.ReviewCreateView.as_view(), name='review_create'),
        path('bookings/', views.BookingListView.as_view(), name='bookings_list'),
        path('monthly-guests/', views.MonthlyGuestListView.as_view(), name='monthly_guests'),
    ]