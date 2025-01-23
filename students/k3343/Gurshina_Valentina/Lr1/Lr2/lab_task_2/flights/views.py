# Create your views here.

from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import RegistrationForm

# РЕГИСТРАЦИЯ / АВТОРИЗАЦИЯ 

def register_request(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("view_flights")
        messages.error(request, "Ошибка регистрации. Проверьте введённые данные и попробуйте снова.")
    else:
        form = RegistrationForm()
    return render(request=request, template_name="flights/register.html", context={"register_form": form})
# render для выведения формы регистрации при отправлении GET-запроса

# ВХОД 

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password) #проверяем корректность данных
            if user:
                login(request, user)
                messages.info(request, f"Вы в системе как {user.last_name} {user.first_name}.")
                return redirect("view_flights")
            else:
                messages.error(request, "Ошибка. Неверный логин или пароль.")
        else:
            messages.error(request, "Ошибка. Неверный логин или пароль.")
    form = AuthenticationForm()
    return render(request=request, template_name="flights/login.html", context={"login_form": form})

# ВЫХОД 

from django.contrib.auth import logout

def logout_request(request):
    logout(request)
    messages.info(request, "Вы вышли из системы. До скорых встреч!")
    return redirect("login")

# ПРОСМОТР / ЧЕК-АП РЕЙСОВ

from django.contrib.auth.decorators import login_required
from .models import Flight

@login_required  #помогает обеспечить доступ к этому представлению только для зарегистрированных и авторизованных пользователей
def view_flights(request):
    flights = Flight.objects.exclude(bookings__user=request.user).filter(date__gt=timezone.now()).order_by("date")
    #исключаем рейсы, на которые уже есть бронь у пользователя
    return render(request, "flights/flights_list.html", {"flights": flights})

# УПРАВЛЕНИЕ БРОНИРОВАНИЕМ

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Booking

@login_required
def view_bookings(request, tab): #позволим просматривать предстоящие и завершенные рейсы
    if tab == "upcoming":
        bookings = Booking.objects.filter(user=request.user, flight__date__gte=timezone.now())
    else:
        bookings = Booking.objects.filter(user=request.user, flight__date__lt=timezone.now())

    return render(request, "flights/my_flights.html", {"bookings": bookings, "active_tab": tab})

#БРОНИРОВАНИЕ

from django.contrib.auth.decorators import login_required

from .models import Flight, Booking

@login_required
def book_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    Booking.objects.create(user=request.user, flight=flight)
    messages.success(request, "Вам удалось забронировать место на рейс.")
    return redirect("view_flights")

# ОТМЕНА/УДАЛЕНИЕ БРОНИ

from django.contrib.auth.decorators import login_required

from .models import Booking

@login_required
def delete_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "Вы отменили бронь.")
    return redirect("view_bookings", "upcoming")

# ОТЗЫВЫ И ОБРАТНАЯ СВЯЗЬ

from django.contrib.auth.decorators import login_required

from .forms import FeedbackForm
from .models import Flight

@login_required
def give_feedback(request, flight_id):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.flight = Flight.objects.get(id=flight_id)
            feedback.save()
            messages.success(request, "Отзыв отправлен. Благодарим за обратную связь, для нас это очень важно!")
            return redirect("view_bookings", "past")
    else:
        form = FeedbackForm()
    return render(request, "flights/feedback.html", {"form": form})

# ИНФОРМАЦИЯ И ДАННЫЕ О РЕЙСЕ

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Flight

@login_required
def flight_details(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    return render(request, "flights/flight_details.html", {"flight": flight})
#если рейса нет, то отправит ошибку 404











