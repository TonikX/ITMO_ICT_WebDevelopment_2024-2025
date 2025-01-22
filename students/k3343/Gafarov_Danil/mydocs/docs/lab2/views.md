# Документация Django проекта

## Описание файлов

### views.py

#### home_view(request)

```python
def home_view(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, "base.html", {"reservations": reservations})
```

Описание: Этот view отображает домашнюю страницу. Он фильтрует бронирования по текущему пользователю и передает их в шаблон "base.html".

#### hotel_list(request)

```python
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, "hotel_list.html", {"hotels": hotels})
```

Описание: Этот view отображает список отелей. Он извлекает все отели из базы данных и передает их в шаблон "hotel_list.html".

#### add_review(request, room_id)

```python
@login_required(login_url="login")
def add_review(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        comment = request.POST["comment"]
        rating = request.POST["rating"]
        review = Review(
            user=request.user,
            room=room,
            comment=comment,
            rating=rating,
        )
        print(review)
        review.save()

        return redirect("hotel_list")
    return render(request, "add_review.html", {"room": room})
```
Описание: Этот view позволяет пользователю добавить отзыв о номере. Если запрос метод POST, то создается новый объект Review с данными от пользователя и сохраняется в базе данных. Затем пользователь перенаправляется на страницу списка отелей. Если запрос метод GET, то отображается шаблон "add_review.html" с передачей объекта комнаты в шаблон.

#### create_hotel(request)

```python
@login_required(login_url="login")
def create_hotel(request):
    if request.method == "POST":
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = form.save()
            return redirect("view_hotel", pk=hotel.pk)
    else:
        form = HotelForm()
    return render(request, "create_hotel.html", {"form": form})
```
Описание: Этот view позволяет пользователю создать новый отель. Если запрос метод POST, то форма формируется из данных запроса и проверяется на валидность. Если форма действительна, создается новый объект Hotel и сохраняется в базе данных, затем пользователь перенаправляется на страницу просмотра отеля. Если запрос метод GET, то отображается шаблон "create_hotel.html" с передачей формы в шаблон.

#### view_hotel(request, pk)

```python
@login_required(login_url="login")
def view_hotel(request, pk):
    hotel = Hotel.objects.get(pk=pk)
    rooms = Room.objects.filter(hotel=hotel)
    reviews = Review.objects.all()
    now = datetime.datetime.now()
    last_month_start = now.replace(day=1) - datetime.timedelta(days=1)
    last_month_end = last_month_start.replace(day=1)

    reservations = Reservation.objects.all()

    return render(
        request,
        "view_hotel.html",
        {
            "hotel": hotel,
            "rooms": rooms,
            "reviews": reviews,
            "reservations": reservations,
        },
    )
```
Описание: Этот view отображает страницу просмотра отеля. Он получает объект отеля по идентификатору, затем извлекает все комнаты отеля и отзывы о нем из базы данных. Также он формирует диапазон последнего месяца и извлекает все бронирования за этот период. Затем он передает объекты отеля, комнат, отзывов и бронирований в шаблон "view_hotel.html".

#### create_room(request, hotel_pk)

```python
@login_required(login_url="login")
def create_room(request, hotel_pk):
    hotel = Hotel.objects.get(pk=hotel_pk)
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            return redirect("view_hotel", pk=hotel.pk)
    else:
        form = RoomForm()
    return render(request, "create_room.html", {"form": form, "hotel": hotel})
```
Описание: Этот view позволяет пользователю создать новый номер в отеле. Если запрос метод POST, то форма формируется из данных запроса и проверяется на валидность. Если форма действительна, создается новый объект Room связанный с объектом отеля и сохраняется в базе данных, затем пользователь перенаправляется на страницу просмотра отеля. Если запрос метод GET, то отображается шаблон "create_room.html" с передачей формы и объекта отеля в шаблон.

#### book_room(request, hotel_pk)

```python
@login_required(login_url="login")
def book_room(request, hotel_pk):
    if request.method == "POST":
        room_id = request.POST["room_id"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]

        hotel = Hotel.objects.get(pk=hotel_pk)

        reservation = Reservation(
            hotel=hotel,
            user=request.user,
            room_id=room_id,
            start_date=start_date,
            end_date=end_date,
        )
        reservation.save()

        room = Room.objects.get(id=room_id)
        room.available = False
        room.save()

        return redirect("reservation_success")
    else:
        hotel = Hotel.objects.get(pk=hotel_pk)
        rooms = Room.objects.filter(hotel=hotel)
        return render(
            request, "room_reservation.html", {"hotel": hotel, "rooms": rooms}
        )
```
Описание: Этот view позволяет пользователю забронировать номер в отеле. Если запрос метод POST, то извлекаются данные о выбранном номере и детали бронирования из данных запроса. Создается новый объект Reservation с этими данными и сохраняется в базе данных. Затем обновляется доступность комнаты. Пользователь перенаправляется на страницу успешного бронирования. Если запрос метод GET, то отображается шаблон "room_reservation.html" с передачей объекта отеля и списка комнат в шаблон.

#### reservation_success(request)

```python
def reservation_success(request):
    return render(request, "reservation_success.html")
```
Описание: Этот view отображает страницу успешного бронирования. Он отображает шаблон "reservation_success.html".

#### register(request)

```python
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect("login")
        print(form)
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})
```
Описание: Этот view позволяет пользователю зарегистрироваться. Если запрос метод POST, то форма формируется из данных запроса и проверяется на валидность. Если форма действительна, создается новый объект пользователя и сохраняется в базе данных, затем пользователь перенаправляется на страницу входа. Если запрос метод GET, то отображается шаблон "accounts/register.html" с передачей формы в шаблон.

#### login_view(request)

```python
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return redirect("login")
    return render(request, "accounts/login.html")
```
Описание: Этот view позволяет пользователю войти в систему. Если запрос метод POST, то извлекаются имя пользователя и пароль из данных запроса. Вход выполняется вызовом функции аутентификации и, при успешном входе, пользователь перенаправляется на домашнюю страницу. В случае неудачи, пользователь перенаправляется на страницу входа. Если запрос метод GET, то отображается шаблон "accounts/login.html".


#### logout_view(request)

```python
@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("login")
```
Описание: Этот view позволяет пользователю выйти из системы.