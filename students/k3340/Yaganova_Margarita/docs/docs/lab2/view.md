# Контроллеры

Для реализации поставленных задач было создано несколько контроллеров, 
обеспечивающих функционал сайта.

### Вход и регистрация

Для реализации данных функция во многом были использованы библиотечные 
функции `django`

```python
class TouristLoginView(LoginView):
    template_name = 'registration/login.html'


class TouristLogoutView(LogoutView):
    template_name = 'registration/logout.html'


def register(request):
    if request.method == 'POST':
        form = TouristRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('account')
    else:
        form = TouristRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
```

### Личный кабинет пользователя

В личном кабинете отображается информация о бронированиях, а также
есть возможность их редактировать, комментировать и удалять

```python
@login_required
def account(request):
    bookings = TourBooking.objects.filter(tourist=request.user)
    return render(request, 'registration/account.html', {'bookings': bookings})
```

Удаление туров:

```python
def delete_booking(request, booking_id):
    booking = TourBooking.objects.get(pk=booking_id)
    if request.method == 'POST':
        booking.delete()
        return redirect('account')
    return redirect('account')
```

### Список туров

На главной странице приложения отображается список доступных туров 
для бронирования

```python
def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'tour_list.html', {'tours': tours})
```

### Детали тура

Также турист может посмотреть подробную информацию о каждом туре, 
а также увидеть комментарии, оставленные другими пользователями

```python
def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    reviews = Review.objects.filter(tour=tour)
    country = Country.objects.filter(tour=tour)[0]
    return render(request, 'tour_detail.html',
                  {'tour': tour, 'reviews': reviews, 'country': country})
```

### Таблица туров

Также есть возможность посмотреть завершеннные бронирования по направлениям,
где отображается название и пользователь, который его бронировал

```python
def tour_table(request):
    country_form = CountrySelectionForm(request.GET)

    if country_form.is_valid():
        country = country_form.cleaned_data['country']
        tours = Tour.objects.filter(country=country)
        completed_bookings = TourBooking.objects.filter(Q(tour__in=tours),
                                                        status="D")
    else:
        completed_bookings = TourBooking.objects.filter(status="D")
    return render(request, 'tour_table.html', {'bookings': completed_bookings,
                                               'country_form': country_form})
```