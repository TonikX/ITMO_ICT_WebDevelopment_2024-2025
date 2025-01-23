# Представления

## Регистрация

```python
class TravelAgency(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()

    def __str__(self):
        return self.name
```

Отвечает за регистрацию новых пользователей. Перенаправляет на страницу входа.

## Вход в систему

```python
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tour_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
```
Использует форму аутентификации для входа пользователя. Перенаправляет на страницу отелей.

## Выход из системы


```python
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
```
Перенаправляет на страницу входа. Только для авторизованных пользоватей.

## Список туров


```python
def tour_list(request):
    form = TourSearchForm(request.GET)
    tours = Tour.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            # Используем Q для поиска по нескольким полям
            tours = tours.filter(
                Q(hotel__icontains=query) |
                Q(country__icontains=query) |
                Q(city__icontains=query) |
                Q(description__icontains=query)
            )

    paginator = Paginator(tours, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tour_list.html', {'page_obj': page_obj, 'form': form})
```

Получает все имеющиеся туры. Так же позволяет совершать поиск по турам (по полям отель, страна, город и описание). Добавляет пагинацию для отображения на странице.


## Детали тура

```python
def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    nights = (tour.end_date - tour.start_date).days
    return render(request, 'tour_detail.html', {'tour': tour, 'nights': nights})
```

Получает детали тура из модели, считает длительность тура.

## Резервирование тура

```python
@login_required
def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, tour=tour)
        print(form.is_valid())
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour
            booking.user = request.user
            booking.save()
            print(booking)
            return redirect('my_bookings')
    else:
        form = BookingForm(tour=tour)
    return render(request, 'book_tour.html', {'form': form, 'tour': tour})
```

Получает данные из формы, создает бронь на определенный тур и перенаправляет на страницу броней пользователя. Только для авторизованных пользоватей.

## Обновление бронирования

```python
class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'update_booking.html'
    success_url = reverse_lazy('my_bookings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tour'] = self.object.tour
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Booking'
        context['total_price'] = self.object.total_price
        return context
```
Получает данные из формы и обновляет бронь пользователя. При успехе перенаправляет на страницу броней пользователя.

## Удаление бронирования

```python
class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'delete_booking.html'
    success_url = reverse_lazy('my_bookings')
    title = 'Booking Cancellation'
```
Удаляет конкретное бронирование. При успехе перенаправляет на страницу бронирований.

## Детали бронирования

```python
class BookingDetailView(DetailView):
    model = Booking
    template_name = 'booking_detail.html'
    context_object_name = 'booking'
```

Получает данные о брони.

## Мои бронирования

```python
@login_required
def my_bookings(request):
    bookings = request.user.bookings.all()
    return render(request, 'my_bookings.html', {'bookings': bookings})
```

Получает все бронирование определенного пользователя. Только для авторизованных пользователей.

## Отзывы

```python
@login_required
def add_review(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if not request.user.bookings.filter(tour=tour, is_confirmed=True).exists():
        return redirect('my_bookings', pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = tour
            review.save()
            return redirect('tour_detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'tour': tour})
```

Создает отзыв на подтвержденную бронь. Только для авторизованных пользователей.

## Добавление тура

```python
@admin_required
def add_tour(request):
    if request.method == 'POST':
        form = TourForm(request.POST)

        if form.is_valid():
            # Сохранение тура перед обработкой формсетов
            tour = form.save(commit=False)
            tour.save()

            # Привязываем сохранённый тур к формсетам
            tariff_formset = TariffFormSet(request.POST, instance=tour)
            meal_option_formset = MealOptionFormSet(request.POST, instance=tour)

            if tariff_formset.is_valid() and meal_option_formset.is_valid():
                tariff_formset.save()
                meal_option_formset.save()
                return redirect('tour_list')
        else:
            # Создание пустых формсетов при ошибке в основной форме
            tariff_formset = TariffFormSet(instance=form.instance)
            meal_option_formset = MealOptionFormSet(instance=form.instance)
    else:
        # Инициализация пустых форм
        form = TourForm()
        tariff_formset = TariffFormSet(instance=Tour())
        meal_option_formset = MealOptionFormSet(instance=Tour())

    return render(request, 'add_tour.html', {
        'form': form,
        'tariff_formset': tariff_formset,
        'meal_option_formset': meal_option_formset,
    })
```
Получает данные из формы, создает тур и создает тарифы и варианты питания для созданного тура. Только для администратора.

## Редактирование тура

```python
@admin_required
def edit_tour(request, pk):
    tour = get_object_or_404(Tour, pk=pk)

    if request.method == 'POST':
        form = TourForm(request.POST, instance=tour)
        tariff_formset = TariffFormSet(request.POST, instance=tour)
        meal_option_formset = MealOptionFormSet(request.POST, instance=tour)

        if form.is_valid() and tariff_formset.is_valid() and meal_option_formset.is_valid():
            # Сохраняем изменения в туре
            form.save()

            for tariff in tariff_formset.save(commit=False):
                tariff.tour = tour
                tariff.save()

            # Удаляем только помеченные для удаления тарифы
            for tariff in tariff_formset.deleted_objects:
                tariff.delete()

            for meal_option in meal_option_formset.save(commit=False):
                meal_option.tour = tour
                meal_option.save()

            # Удаляем только помеченные для удаления варианты питания
            for meal_option in meal_option_formset.deleted_objects:
                meal_option.delete()

            return redirect('tour_list')

    else:
        form = TourForm(instance=tour)
        tariff_formset = TariffFormSet(instance=tour)
        meal_option_formset = MealOptionFormSet(instance=tour)

    return render(request, 'edit_tour.html', {
        'form': form,
        'tariff_formset': tariff_formset,
        'meal_option_formset': meal_option_formset,
    })
```

Получает данные из формы и обновляет данные о туре, добавляет тарифы и опции и удаляет помеченное. Только для администратора.

## Просмотр бронирований администратором

```python
@admin_required
def view_bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'view_bookings.html', {'bookings': bookings})
```

Возвращает бронирования всех пользователей. Только для администратора.

## Подтверждение бронирований пользователей

```python
@admin_required
def confirm_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.is_confirmed = True
    booking.save()
    return redirect('view_bookings')
```

Подтвержает бронирование пользователей, перенаправляет на страницу бронирований пользоватей. Только для администратора.

## Проданные туры по странам

```python
@admin_required
def sold_tours_by_country(request):
    tours_by_country = (
        Tour.objects.filter(bookings__is_confirmed=True)
        .values('country')
        .annotate(total_bookings=Count('bookings'))
        .order_by('-total_bookings')
    )
    return render(request, 'sold_tours.html', {'tours_by_country': tours_by_country})
```
Фильтрует туры и по странам и считает количество подтвержденных бронирований для каждой страны. Только для администратора.