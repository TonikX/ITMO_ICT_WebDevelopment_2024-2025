from django.forms import IntegerField
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from django.db.models import Q, Count, Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import ExtractQuarter, ExtractYear
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from django.db.models.functions import Cast
from django.db.models import Func, Value


from .models import (
    RoomType, Room, Guest, Booking, Employee, CleaningAssignment
)
from .serializers import (
    RoomTypeSerializer, RoomSerializer, GuestSerializer,
    BookingSerializer, EmployeeSerializer, CleaningAssignmentSerializer
)



class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'], url_path='free')
    def free_rooms(self, request):
        today = date.today()

        # Номера, которые НЕ заняты на сегодня:
        # - нет активных Booking (check_in <= today и (check_out > today или check_out is null))
        occupied_ids = Booking.objects.filter(
            Q(check_in__lte=today) &
            (Q(check_out__gt=today) | Q(check_out__isnull=True))
        ).values_list('room_id', flat=True).distinct()

        free_rooms = Room.objects.exclude(id__in=occupied_ids)

        serializer = RoomSerializer(free_rooms, many=True)
        return Response({
            "date": str(today),
            "free_count": free_rooms.count(),
            "free_rooms": serializer.data
        })

    @action(detail=True, methods=['get'], url_path='guests-in-period')
    def guests_in_period(self, request, pk=None):
        room = self.get_object()

        start_str = request.query_params.get('start')
        end_str = request.query_params.get('end')

        if not start_str or not end_str:
            return Response(
                {"detail": "Обязательные параметры: ?start=YYYY-MM-DD&end=YYYY-MM-DD"},
                status=400
            )

        try:
            start = datetime.strptime(start_str, '%Y-%m-%d').date()
            end = datetime.strptime(end_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Неверный формат даты. Используйте YYYY-MM-DD"}, status=400)

        if start > end:
            return Response({"detail": "start должна быть раньше end"}, status=400)

        # Бронирования, которые пересекаются с периодом [start, end]
        # Условие: бронь началась до конца периода И закончилась после начала периода
        overlapping_bookings = Booking.objects.filter(
            Q(room=room) &
            Q(check_in__lte=end) &
            (Q(check_out__gt=start) | Q(check_out__isnull=True))
        )

        # Получаем уникальных гостей
        guests = Guest.objects.filter(
            bookings__in=overlapping_bookings
        ).distinct()

        serializer = GuestSerializer(guests, many=True)

        return Response({
            "room": RoomSerializer(room).data,
            "period": {
                "start": str(start),
                "end": str(end)
            },
            "guests_count": guests.count(),
            "guests": serializer.data
        })


class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['city', 'last_name', 'first_name', 'passport']

    @action(detail=True, methods=['get'], url_path='overlapping-guests')
    def overlapping_guests(self, request, pk=None):
        guest = self.get_object()

        # Получаем все бронирования заданного клиента
        my_bookings = Booking.objects.filter(guest=guest)

        if not my_bookings.exists():
            return Response({"detail": "У этого гостя нет бронирований"}, status=200)

        overlapping_bookings = Booking.objects.none()

        for my_booking in my_bookings:
            # Ищем другие бронирования в том же номере с пересечением дат
            overlap = Booking.objects.filter(
                room=my_booking.room,
                check_in__lte=my_booking.check_out or date.today(),  # до конца моей брони или сегодня
                check_out__gte=my_booking.check_in,  # начало их брони после моего начала
            ).exclude(guest=guest)  # исключаем самого себя
            overlapping_bookings = overlapping_bookings | overlap

        # Получаем уникальных гостей
        overlapping_guests = Guest.objects.filter(
            bookings__in=overlapping_bookings
        ).distinct()

        serializer = GuestSerializer(overlapping_guests, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__iexact=city)  # нечувствительно к регистру
        return queryset


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = [
        'guest__last_name', 'guest__first_name', 'guest__patronymic', 'guest__passport',
        'room__number'
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Дополнительные фильтры, если нужно
        return queryset.order_by('-check_in')

    @action(detail=True, methods=['get'], url_path='cleaner-on-day')
    def cleaner_on_day(self, request, pk=None):
        booking = self.get_object()
        day_of_week = request.query_params.get('day_of_week')  # ?day_of_week=0 (понедельник)

        if not day_of_week:
            return Response({"detail": "Укажите параметр day_of_week (0-6)"}, status=400)

        try:
            day_of_week = int(day_of_week)
            if day_of_week < 0 or day_of_week > 6:
                raise ValueError
        except ValueError:
            return Response({"detail": "day_of_week должен быть числом от 0 до 6"}, status=400)

        floor = booking.room.floor

        cleaners = Employee.objects.filter(
            cleaning_assignments__floor=floor,
            cleaning_assignments__day_of_week=day_of_week
        ).distinct()

        serializer = EmployeeSerializer(cleaners, many=True)
        return Response({
            "booking": BookingSerializer(booking).data,
            "day_of_week": dict(CleaningAssignment.DAYS_OF_WEEK)[day_of_week],
            "floor": floor,
            "cleaners": serializer.data
        })


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CleaningAssignmentViewSet(viewsets.ModelViewSet):
    queryset = CleaningAssignment.objects.all()
    serializer_class = CleaningAssignmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


from collections import defaultdict
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db.models import Count, Q, Sum, F
from django.db.models import Value, DecimalField, ExpressionWrapper
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class QuarterReportView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        year = int(request.query_params.get('year', date.today().year))
        quarter = int(request.query_params.get('quarter', 1))

        if quarter not in [1, 2, 3, 4]:
            return Response({"detail": "quarter должен быть 1-4"}, status=400)

        quarter_start = date(year, (quarter - 1) * 3 + 1, 1)
        quarter_end = quarter_start + relativedelta(months=3) - relativedelta(days=1)

        today = date.today()

        # Клиенты по номерам (пересечение периодов)
        clients_per_room = Booking.objects.filter(
            Q(check_in__lte=quarter_end),
            Q(check_out__gte=quarter_start) | Q(check_out__isnull=True)
        ).values(
            'room__number', 'room__floor'
        ).annotate(
            client_count=Count('guest', distinct=True)
        ).order_by('room__number')

        rooms_per_floor = Room.objects.values('floor').annotate(count=Count('id'))

        revenue_dict = defaultdict(float)

        # Завершённые брони
        completed = Booking.objects.filter(
            check_in__lte=quarter_end,
            check_out__gte=quarter_start,
            check_out__isnull=False
        ).select_related('room__room_type')

        for b in completed:
            days = (b.check_out - b.check_in).days
            if days > 0:
                price = b.room.room_type.price_per_day
                revenue_dict[b.room.number] += float(days * price)

        # Активные брони (до today)
        active = Booking.objects.filter(
            check_in__lte=quarter_end,
            check_out__isnull=True
        ).filter(
            check_in__lte=today  # отдельный filter — без дублирования
        ).select_related('room__room_type')

        for b in active:
            days = (today - b.check_in).days
            if days > 0:
                price = b.room.room_type.price_per_day
                revenue_dict[b.room.number] += float(days * price)

        revenue_per_room = [
            {'room__number': number, 'revenue': revenue}
            for number, revenue in revenue_dict.items()
        ]

        total_revenue = sum(revenue for revenue in revenue_dict.values())

        return Response({
            "year": year,
            "quarter": quarter,
            "period": {
                "start": str(quarter_start),
                "end": str(quarter_end)
            },
            "rooms_per_floor": list(rooms_per_floor),
            "clients_per_room": list(clients_per_room),
            "revenue_per_room": revenue_per_room,
            "total_revenue": float(total_revenue)
        })