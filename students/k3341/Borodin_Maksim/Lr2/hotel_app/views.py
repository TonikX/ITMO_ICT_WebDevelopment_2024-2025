from datetime import timedelta
from typing import Any, Dict, Optional

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q, QuerySet, Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.cache import cache_page

from .models import Hotel, Room, Reservation, Review, Amenity
from .forms import SignUpForm, ReservationForm, ReviewForm


class SignUpView(CreateView):
    """
    Представление для регистрации новых пользователей.
    После успешной регистрации автоматически выполняет вход пользователя.
    """
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('hotel_list')

    @transaction.atomic
    def form_valid(self, form: SignUpForm) -> HttpResponse:
        """Сохраняет форму и выполняет вход пользователя."""
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Добро пожаловать! Регистрация успешно завершена.')
        return response


@method_decorator(cache_page(60 * 15), name='dispatch')  # Кэширование на 15 минут
class HotelListView(ListView):
    """
    Отображает список отелей с пагинацией и возможностью поиска.
    Кэширует результаты на 15 минут для улучшения производительности.
    """
    model = Hotel
    template_name = 'hotel_list.html'
    context_object_name = 'hotels'
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        """
        Возвращает отфильтрованный и отсортированный список отелей.
        Поддерживает поиск по названию или адресу и сортировку.
        """
        qs = super().get_queryset().prefetch_related(
            Prefetch('amenities', queryset=Amenity.objects.only('name'))
        )
        
        # Поиск
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(name__icontains=q) | 
                Q(address__icontains=q)
            )
        
        # Сортировка
        sort = self.request.GET.get('sort', 'name')  # по умолчанию по названию
        if sort == 'name':
            qs = qs.order_by('name')
        elif sort == '-name':
            qs = qs.order_by('-name')
        
        return qs.select_related('owner')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Добавляет параметры сортировки в контекст."""
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', 'name')
        return context


class HotelDetailView(DetailView):
    """
    Детальное представление отеля с информацией о номерах и постояльцах.
    Включает список всех номеров отеля и постояльцев за последний месяц.
    """
    model = Hotel
    template_name = 'hotel_detail.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Расширяет контекст данными о номерах и постояльцах.
        Оптимизирует запросы с помощью select_related и prefetch_related.
        """
        ctx = super().get_context_data(**kwargs)
        
        # Предзагружаем все связанные данные для номеров
        ctx['rooms'] = self.object.rooms.filter(
            is_active=True
        ).select_related(
            'room_type'
        ).prefetch_related(
            Prefetch('amenities', queryset=Amenity.objects.only('name'))
        )

        # Получаем список постояльцев за последний месяц
        now = timezone.now().date()
        month_ago = now - timedelta(days=30)
        
        guests = (Reservation.objects
            .select_related('user', 'room')
            .filter(
                room__hotel=self.object,
                status__in=[
                    Reservation.Status.CHECKED_IN,
                    Reservation.Status.CHECKED_OUT
                ],
                check_in__lte=now,
                check_out__gte=month_ago
            )
            .order_by('-check_in')
        )
        ctx['recent_guests'] = guests
        
        return ctx

class RoomDetailView(DetailView):
    """
    Детальное представление номера с формами бронирования и отзывов.
    Отображает информацию о номере, все отзывы и формы для создания брони и отзыва.
    """
    model = Room
    template_name = 'room_detail.html'
    context_object_name = 'room'

    def get_queryset(self) -> QuerySet:
        """Оптимизирует запрос с предзагрузкой связанных данных."""
        return super().get_queryset().select_related(
            'hotel',
            'room_type'
        ).prefetch_related('amenities')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Расширяет контекст формами для бронирования и отзывов,
        а также списком существующих отзывов.
        """
        ctx = super().get_context_data(**kwargs)
        
        # Форма бронирования с предзаполненным номером
        ctx['reservation_form'] = ReservationForm(initial={
            'room': self.object,
            'check_in': timezone.now().date(),
            'check_out': timezone.now().date() + timedelta(days=1)
        })

        # Отзывы с пагинацией и сортировкой
        ctx['reviews'] = (
            self.object.reviews
            .select_related('user')
            .order_by('-created_at')
        )

        # Форма отзыва только для авторизованных пользователей
        if self.request.user.is_authenticated:
            ctx['review_form'] = ReviewForm(initial={'room': self.object})
        
        return ctx

class MyReservationsView(LoginRequiredMixin, ListView):
    """
    Отображает список бронирований текущего пользователя.
    Доступно только авторизованным пользователям.
    """
    model = Reservation
    template_name = 'reservations/my_reservations.html'
    context_object_name = 'reservations'
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        """
        Возвращает отфильтрованный и отсортированный список бронирований
        текущего пользователя с предзагруженными связанными данными.
        """
        return (Reservation.objects
            .select_related('room__hotel', 'room__room_type')
            .filter(user=self.request.user)
            .order_by('-created_at')
        )

class ReservationCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового бронирования.
    Доступно только авторизованным пользователям.
    """
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_form.html'
    success_url = reverse_lazy('my_reservations')

    @transaction.atomic
    def form_valid(self, form: ReservationForm) -> HttpResponse:
        """
        Сохраняет новое бронирование, привязывая его к текущему пользователю.
        Проверяет доступность номера перед сохранением.
        """
        form.instance.user = self.request.user
        
        # Проверяем, активен ли номер
        if not form.instance.room.is_active:
            form.add_error('room', 'Этот номер временно недоступен для бронирования')
            return self.form_invalid(form)
        
        response = super().form_valid(form)
        messages.success(self.request, 'Бронирование успешно создано')
        return response

class OwnReservationMixin(UserPassesTestMixin):
    """
    Миксин для проверки, принадлежит ли бронирование текущему пользователю
    и может ли оно быть отредактировано.
    """
    def test_func(self) -> bool:
        """
        Проверяет, что бронирование принадлежит текущему пользователю
        и находится в статусе, допускающем редактирование.
        """
        reservation = self.get_object()
        if reservation.user != self.request.user:
            return False
        
        if isinstance(self, ReservationUpdateView) and not reservation.can_be_edited():
            messages.error(
                self.request,
                'Бронирование нельзя редактировать в текущем статусе'
            )
            return False
            
        if isinstance(self, ReservationDeleteView) and not reservation.can_be_cancelled():
            messages.error(
                self.request,
                'Бронирование нельзя отменить в текущем статусе'
            )
            return False
            
        return True

class ReservationUpdateView(LoginRequiredMixin, OwnReservationMixin, UpdateView):
    """
    Представление для редактирования существующего бронирования.
    Доступно только владельцу бронирования и только для определенных статусов.
    """
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_form.html'
    success_url = reverse_lazy('my_reservations')

    def get_queryset(self) -> QuerySet:
        """Оптимизирует запрос с предзагрузкой связанных данных."""
        return super().get_queryset().select_related('room__hotel')

    @transaction.atomic
    def form_valid(self, form: ReservationForm) -> HttpResponse:
        """Сохраняет изменения в бронировании после валидации."""
        response = super().form_valid(form)
        messages.success(self.request, 'Бронирование успешно обновлено')
        return response

class ReservationDeleteView(LoginRequiredMixin, OwnReservationMixin, DeleteView):
    """
    Представление для отмены бронирования.
    Доступно только владельцу бронирования и только для определенных статусов.
    """
    model = Reservation
    template_name = 'reservations/reservation_confirm_delete.html'
    success_url = reverse_lazy('my_reservations')

    def get_queryset(self) -> QuerySet:
        """Оптимизирует запрос с предзагрузкой связанных данных."""
        return super().get_queryset().select_related('room__hotel')

    @transaction.atomic
    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Отменяет бронирование и показывает сообщение об успехе."""
        messages.success(request, 'Бронирование успешно отменено')
        return super().delete(request, *args, **kwargs)

class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового отзыва о номере.
    Доступно только авторизованным пользователям, которые проживали в номере.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def get_success_url(self) -> str:
        """Возвращает URL страницы номера после создания отзыва."""
        return reverse_lazy('room_detail', kwargs={'pk': self.object.room_id})

    def form_valid(self, form: ReviewForm) -> HttpResponse:
        """
        Сохраняет новый отзыв, привязывая его к текущему пользователю.
        """
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Спасибо! Ваш отзыв успешно добавлен')
        return response

    @transaction.atomic
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Обрабатывает POST-запрос. Устанавливает пользователя перед валидацией формы.
        """
        self.object = None
        form = self.get_form()
        form.instance.user = request.user
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

