from requests import Response
from rest_framework import viewsets
from django.db.models import Q
from . import models
from .models import UserAccount, Room, RoomType, RoomTypePrice, Employee, Position, SalaryHistory, Contract, WorkSchedule, Booking
from .serializers import UserAccountSerializer, RoomSerializer, RoomTypeSerializer, RoomTypePriceSerializer, EmployeeSerializer, PositionSerializer, SalaryHistorySerializer, ContractSerializer, WorkScheduleSerializer, BookingSerializer
from django.db.models import Count
from django.http import JsonResponse
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status


class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


class RoomTypePriceViewSet(viewsets.ModelViewSet):
    queryset = RoomTypePrice.objects.all()
    serializer_class = RoomTypePriceSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class SalaryHistoryViewSet(viewsets.ModelViewSet):
    queryset = SalaryHistory.objects.all()
    serializer_class = SalaryHistorySerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class WorkScheduleViewSet(viewsets.ModelViewSet):
    queryset = WorkSchedule.objects.all()
    serializer_class = WorkScheduleSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


def clients_per_room(request):
    start_date = request.GET.get('start_date', '2024-01-01')
    end_date = request.GET.get('end_date', '2024-12-31')

    # Преобразуем строки в объекты datetime
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Выполняем аннотацию и фильтрацию
    rooms_with_clients = Room.objects.annotate(
        client_count=Count('bookings', filter=(
            Q(bookings__check_in_time__gte=start_date) &
            Q(bookings__departure_time__lte=end_date)
        ))
    )

    # Формируем результат
    result = [
        {"room_number": room.number, "client_count": room.client_count or 0}
        for room in rooms_with_clients
    ]

    return JsonResponse(result, safe=False)


def rooms_per_floor(request):
    floors = (
        Room.objects.values('floor')
        .annotate(room_count=Count('id'))
        .order_by('floor')
    )

    result = [
        {"floor": floor['floor'], "room_count": floor['room_count']}
        for floor in floors
    ]

    return JsonResponse(result, safe=False)


def total_income_per_room(request):
    start_date = request.GET.get('start_date', '2024-01-01')
    end_date = request.GET.get('end_date', '2024-12-31')

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    rooms = Room.objects.all()
    income_data = []

    for room in rooms:
        bookings = Booking.objects.filter(
            room=room,
            check_in_time__gte=start_date,
            departure_time__lte=end_date
        )
        total_income = 0
        for booking in bookings:
            price_entry = room.room_type.prices.filter(
                start_date__lte=booking.booking_date,
                end_date__gte=booking.booking_date
            ).first()
            if price_entry:
                total_income += booking.full_days * price_entry.day_price
        income_data.append({"room_number": room.number, "total_income": total_income})

    return JsonResponse(income_data, safe=False)



def total_income(request):
    start_date = request.GET.get('start_date', '2024-01-01')
    end_date = request.GET.get('end_date', '2024-12-31')

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    bookings = Booking.objects.filter(
        check_in_time__gte=start_date,
        departure_time__lte=end_date
    )

    total_income = sum([
        booking.full_days * booking.room.room_type.prices.filter(
            start_date__lte=booking.booking_date,
            end_date__gte=booking.booking_date
        ).first().day_price
        for booking in bookings
    ])

    return JsonResponse({"total_income": total_income})


def clients_in_room(request):
    room_number = request.GET.get('room_number')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    bookings = Booking.objects.filter(
        room__number=room_number,
        check_in_time__gte=start_date,
        departure_time__lte=end_date
    ).select_related('client')

    result = [
        {
            "client_name": f"{booking.client.firstname} {booking.client.lastname}",
            "email": booking.client.email,
            "phone": booking.client.phone
        }
        for booking in bookings
    ]

    return JsonResponse(result, safe=False)


def clients_from_city(request):
    city_name = request.GET.get('city_name')
    client_count = Booking.objects.filter(from_town=city_name).values('client').distinct().count()

    return JsonResponse({"city_name": city_name, "client_count": client_count})


def free_rooms_count(request):
    free_rooms = Room.objects.filter(is_occupied=False).count()

    return JsonResponse({"free_rooms": free_rooms})
