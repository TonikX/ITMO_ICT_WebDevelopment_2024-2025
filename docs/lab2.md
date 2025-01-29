# Лабораторная работа 2
Хранится информация о названии тура, турагенстве, описании тура, периоде
проведения тура, условиях оплаты.
Необходимо реализовать следующий функционал:
  Регистрация новых пользователей.
  Просмотр и резервирование туров. Пользователь должен иметь возможность
  редактирования и удаления своих резервирований.
  Написание отзывов к турам. При добавлении комментариев, должны
сохраняться даты тура, текст комментария, рейтинг (1-10), информация о
комментаторе.
  Администратор должен иметь возможность подтвердить резервирование
тура средствами Django-admin.
  В клиентской части должна формироваться таблица, отображающая все
проданные туры по странам.
## Модели

# Тур
    class Tour(models.Model):
        name = models.CharField(max_length=200)
        agency = models.CharField(max_length=200)
        description = models.TextField()
        period = models.CharField(max_length=200)
        payment_conditions = models.TextField()

    def __str__(self):
        return self.name

# Бронирование

    class Reservation(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
        reserved_on = models.DateTimeField(auto_now_add=True)
        is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Бронирование {self.tour.name} для {self.user.username}"
        
# Отзыв

    class Review(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
        text = models.TextField()  # Текст отзыва
        rating = models.PositiveSmallIntegerField(default=1)
        created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.tour.name}"

## Представления

# Тур - лист
    def tour_list(request):
        tours = Tour.objects.all()
        return render(request, 'tours/tour_list.html', {'tours': tours})

# Детали тура

    def tour_detail(request, tour_id):
        tour = get_object_or_404(Tour, id=tour_id)
        reviews = Review.objects.filter(tour=tour)

        is_reserved = False
        if request.user.is_authenticated:
            is_reserved = Reservation.objects.filter(user=request.user, tour=tour).exists()
    
        return render(request, 'tours/tour_detail.html', {
            'tour': tour,
            'reviews': reviews,
            'is_reserved': is_reserved
        })

# Отмена регистрации

    @login_required
    def cancel_reservation(request, tour_id):
        tour = get_object_or_404(Tour, id=tour_id)

        reservation = Reservation.objects.filter(user=request.user, tour=tour).first()
        if reservation:
            reservation.delete()
    
        return redirect('tour_detail', tour_id=tour.id)

# Бронирование тура

    @login_required
    def reserve_tour(request, tour_id):
        tour = get_object_or_404(Tour, id=tour_id)
        if Reservation.objects.filter(user=request.user, tour=tour).exists():
            return redirect('tour_detail', tour_id=tour.id)
        Reservation.objects.create(user=request.user, tour=tour)
        return redirect('tour_detail', tour_id=tour.id)

# Добавление отзыва

    @login_required
    def add_review(request, tour_id):
        tour = get_object_or_404(Tour, id=tour_id)
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.tour = tour
                review.save()
                return redirect('tour_detail', tour_id=tour.id)
        else:
            form = ReviewForm()
        return render(request, 'tours/add_review.html', {'form': form, 'tour': tour})
    
# Регистрация

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Вход после регистрации
            return redirect('tour_list')  # Замените 'home' на вашу главную страницу
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})
    
# Вход

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tour_list')  # Замените 'home' на вашу главную страницу
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

## Пути

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('',include('tours.urls')),
        path('logout/', views.custom_logout, name='logout'),  # Маршрут для выхода
        path('login/', LoginView.as_view(), name='login'),
        path('', views.tour_list, name='tour_list'),
        path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
        path('tour/<int:tour_id>/reserve/', views.reserve_tour, name='reserve_tour'),
        path('tour/<int:tour_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
        path('register/', views.register, name='register'),
        path('tour/<int:tour_id>/add_review/', views.add_review, name='add_review')
    ]


---

[Назад к главной странице](index.md)
