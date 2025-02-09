Номер в журнале: 21
Вариант 3

Табло отображения информации об авиаперелетах.
Хранится информация о номере рейса, авиакомпании, отлете, прилете, типе
(прилет, отлет), номере гейта.

Необходимо реализовать следующий функционал:
- Регистрация новых пользователей.
- Просмотр и резервирование мест на рейсах. Пользователь должен иметь
возможность редактирования и удаления своих резервирований.
- Администратор должен иметь возможность зарегистрировать на рейс
пассажира и вписать в систему номер его билета средствами Django-admin.
- В клиентской части должна формироваться таблица, отображающая всех
пассажиров рейса.
- Написание отзывов к рейсам. При добавлении комментариев, должны
сохраняться дата рейса, текст комментария, рейтинг (1-10), информация о
комментаторе.

### Ход работы
В первую очередь я заполнил модель данных создав сущности:
- Flight
- Reservation
- Comment

```python
class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.CharField(max_length=50)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    gate = models.CharField(max_length=10)
    arrival_iata = models.CharField(max_length=3)
    departure_iata = models.CharField(max_length=3)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat = models.CharField(max_length=5)
    service_class = models.CharField(max_length=10)
    ticket_number = models.CharField(max_length=20, blank=True, null=True)

class Comment(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
```

Позже, когда проверял работу на соответствование требованиям работу решил добавить в бронирования
информацию об имени и фамилии пассажира. Эта информация не в пользователей,
так как имеет смысл создавать брони разным людям от лица одного пользователя.

Потом по примеру из практической работы я добавил функционал администраторской панели,
внеся нужные изменения в settings и добавив все модели в admin.py

Для того чтобы пользователи могли логиниться я использовал встроенный в Django функционал.
Мне пришлось достать template для окон логина и регистрации. Чтобы не делать их самому
я взял готовые [отсюда](https://github.com/macdhuibh/django-registration-templates/tree/master)

Потом я донастроил эти template немного под себя. Установил django-registration и
по гайду с официальной страницы документации настроил его. Был использован one-step регистрация, без какой либо активации почты.

Некоторое время боролся с возникающими проблемами. Пришлось в settings.py настроить LOGIN_REDIRECT_URL
и ACCOUNT_ACTIVATION_DAYS. После этого все заработало.

Потом я начал делать все view для реализации требуемого функционала.
Для отображения полётов на главной странице использовал ListView.
```python
class FlightListView(ListView):
    model = Flight
    template_name = 'flights/flight_list.html'
    context_object_name = 'flights'
```

Для отображения деталей полёта использовал DetailView. Чтобы не делать много отдельных страничек
я прямо на этой странице решил отображать и бронирования, и комментарии.
```python
class FlightDetailView(DetailView):
    model = Flight
    template_name = 'flights/flight_detail.html'
    context_object_name = 'flight'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flight = self.get_object()
        context['reservations'] = Reservation.objects.filter(flight=flight)
        context['comments'] = Comment.objects.filter(flight=flight).order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context
```

Для бронирования мест создал view:
```python
@login_required
def create_reservation(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.flight = flight
            reservation.save()
            messages.success(request, 'Бронирование успешно создано.')
            return redirect('flight_detail', pk=flight.id)
    else:
        form = ReservationForm()
    return render(request, 'flights/reservation_form.html', {'form': form, 'flight': flight})


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'flights/reservation_form.html'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flight"] = self.object.flight
        return context

    def get_success_url(self):
        return reverse_lazy('flight_detail', kwargs={'pk': self.object.flight.id})


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'flights/reservation_confirm_delete.html'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('flight_detail', kwargs={'pk': self.object.flight.id})
```

Здесь долго боролся с тем, чтобы пользователь мог удалять только свои брони и редактировать тоже только свои,
добавил для этого везде.

```python
def get_queryset(self):
    return Reservation.objects.filter(user=self.request.user)
```

Потом долго разбирался с тем, что почему-то не раотало окно редактирования брони. Оказалось,
что там не было объекта полёта и из-за этого не работало. Добавил его в контекст.

Для создания комментариев использовал:
```python
@login_required
def create_comment(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.flight = flight
            comment.user = request.user
            comment.save()
            messages.success(request, 'Отзыв успешно добавлен.')
        else:
            messages.error(request, 'Ошибка при заполнении формы отзыва.')
    return redirect('flight_detail', pk=flight.id)
```

Не мог разобраться как не заставлять юзера указывать полёт и самого себя, раз информация об этом есть.
Узнал о form.save(commit=False) и добавил это в код.

Потом я долго делал шаблоны. Базовый шаблон с шапкой и шаблон для информации о полёте
пришлось сгенерировать через LLM, потому что мои выглядели очень плохо.

Тут я вспомнил об именах и фамилиях для бронирования и начал всё это добавлять.
Решил, что имя и фамилия отображаются только владельцу бронирования. Потом всё проверил, 
сделал тестовый полёт, пользователей, создал бронирование и убедился, что всё работает.

### Листинг кода
models.py
```python
from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.CharField(max_length=50)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    gate = models.CharField(max_length=10)
    arrival_iata = models.CharField(max_length=3)
    departure_iata = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.flight_number} ({self.airline})"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat = models.CharField(max_length=5)
    service_class = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    ticket_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Бронирование пользователя {self.user.username} на рейс {self.flight.flight_number}"

class Comment(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв {self.rating} от {self.user.username} к рейсу {self.flight.flight_number}"
```

views.py
```python
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Flight, Reservation, Comment
from .forms import ReservationForm, CommentForm


class FlightListView(ListView):
    model = Flight
    template_name = 'flights/flight_list.html'
    context_object_name = 'flights'


class FlightDetailView(DetailView):
    model = Flight
    template_name = 'flights/flight_detail.html'
    context_object_name = 'flight'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flight = self.get_object()
        context['reservations'] = Reservation.objects.filter(flight=flight)
        context['comments'] = Comment.objects.filter(flight=flight).order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context


@login_required
def create_reservation(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.flight = flight
            reservation.save()
            messages.success(request, 'Бронирование успешно создано.')
            return redirect('flight_detail', pk=flight.id)
    else:
        form = ReservationForm()
    return render(request, 'flights/reservation_form.html', {'form': form, 'flight': flight})


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'flights/reservation_form.html'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flight"] = self.object.flight  # Ensure flight is passed
        return context

    def get_success_url(self):
        return reverse_lazy('flight_detail', kwargs={'pk': self.object.flight.id})


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'flights/reservation_confirm_delete.html'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('flight_detail', kwargs={'pk': self.object.flight.id})


@login_required
def create_comment(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.flight = flight
            comment.user = request.user
            comment.save()
            messages.success(request, 'Отзыв успешно добавлен.')
        else:
            messages.error(request, 'Ошибка при заполнении формы отзыва.')
    return redirect('flight_detail', pk=flight.id)
```

forms.py
```python
from django import forms
from .models import Reservation, Comment


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['seat', 'service_class', 'name', 'surname']
        widgets = {
            'seat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер места'}),
            'service_class': forms.Select(attrs={'class': 'form-control'}, choices=(
                ('economy', 'Эконом'),
                ('business', 'Бизнес'),
                ('first', 'Первый'),
            )),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
        }


class CommentForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Рейтинг от 1 до 10'})
    )

    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваш отзыв'}),
        }
```