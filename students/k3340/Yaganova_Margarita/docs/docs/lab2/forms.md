# Формы

Для полной функциональности сайта были реализованы несколько форм

### Бронирование

У пользователя есть возможность забронировать понравившийся тур в 
соответствующей форме

```python
class BookingForm(forms.ModelForm):
    tour_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        tour_id = kwargs.pop('tour_id', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        if tour_id:
            tour = Tour.objects.get(pk=tour_id)
            available_dates = [(date, date) for date in tour.available_dates]
            hotel_categories = [(category, category) for category in
                                tour.hotel_category]
            self.fields['selected_date'] = forms.ChoiceField(
                label='Выберите дату',
                choices=available_dates,
                widget=forms.Select(
                    attrs={'class': 'form-control'}))
            self.fields['selected_category'] = forms.ChoiceField(
                label='Категория отеля',
                choices=hotel_categories,
                widget=forms.Select(
                    attrs={'class': 'form-control'}))

    persons_number = forms.IntegerField(label='Количество взрослых',
                                        widget=forms.NumberInput(
                                            attrs={'class': 'form-control'}))

    children_number = forms.IntegerField(label='Количество детей',
                                         widget=forms.NumberInput(
                                             attrs={'class': 'form-control'}))
    rooms_number = forms.IntegerField(label='Количество номеров',
                                      widget=forms.NumberInput(
                                          attrs={'class': 'form-control'}))
```

```python
def booking(request, tour_id):
    if not request.user.is_authenticated:
        return redirect('login')
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            tour_booking = form.save(commit=False)
            tour_booking.tourist = request.user
            tour_booking.status = 'W'
            tour_booking.tour_id = tour.pk
            tour_booking.save()
            return redirect('account')
    else:
        form = BookingForm(initial={'tour_id': tour_id}, tour_id=tour_id)
    return render(request, 'booking.html', {'form': form})
```

### Комментирование

Также пользователь может комментировать те туры, которые забронировал

```python
class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('rating','text')
```

```python
    if not request.user.is_authenticated:
        return redirect('login')
    tour = get_object_or_404(Tour, pk=tour_id)
    booking = get_object_or_404(TourBooking, pk=booking_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tourist = request.user
            review.tour = tour
            review.booking = booking
            review.save()
            return redirect('account')
    else:
        form = ReviewForm()
    return render(request, 'review.html', {'form': form})
```

### Редактирование бронирования

Для редактирования бронирования используется та жк форма, что и для
простого бронирования, но используется другой контроллер

```python
def edit_tour(request, booking_id):
    booking = get_object_or_404(TourBooking, id=booking_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            tour_booking = form.save(commit=False)
            tour_booking.status = 'W'
            tour_booking.save()
            return redirect('account')
    else:
        form = BookingForm(instance=booking, initial={'tour_id': booking.tour.pk},
                           tour_id=booking.tour.pk)
    return render(request, 'edit_tour.html', {'form': form, 'tour': booking})
```