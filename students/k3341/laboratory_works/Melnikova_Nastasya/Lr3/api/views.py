from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter


from django.db.models import Q
from datetime import date

from .models import Room, Guest, Stay, Staff, CleaningSchedule
from .serializers import (
    RoomSerializer,
    GuestSerializer,
    StaySerializer,
    StaffSerializer,
    CleaningScheduleSerializer
)

# =========================
# ROOMS
# =========================

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=False, methods=['get'])
    def free(self, request):
        occupied_rooms = Stay.objects.filter(
            check_out__isnull=True
        ).values_list('room', flat=True)

        free_rooms = Room.objects.exclude(id__in=list(occupied_rooms))

        serializer = RoomSerializer(free_rooms, many=True)
        return Response(serializer.data)


# =========================
# GUESTS
# =========================

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name='city', type=str, required=True),
        ]
    )
    @action(detail=False, methods=['get'])
    def by_city(self, request):
        city = request.query_params.get('city')
        count = Guest.objects.filter(city_from=city).count()

        return Response({
            "city": city,
            "count": count
        })


# =========================
# STAYS
# =========================

class StayViewSet(viewsets.ModelViewSet):
    queryset = Stay.objects.all()
    serializer_class = StaySerializer

    # 🔥 Клиенты по номеру за период
    @extend_schema(
        parameters=[
            OpenApiParameter(name='room', type=int, required=True),
            OpenApiParameter(name='from', type=str, required=True),
            OpenApiParameter(name='to', type=str, required=True),
        ]
    )
    @action(detail=False, methods=['get'])
    def by_room(self, request):

        room_number = request.query_params.get('room')
        date_from = request.query_params.get('from')
        date_to = request.query_params.get('to')

        if not room_number or not date_from or not date_to:
            return Response(
                {"error": "room, from, to are required"},
                status=400
            )

        stays = Stay.objects.filter(
            room__number=room_number,
            check_in__lte=date_to
        ).filter(
            Q(check_out__isnull=True) | Q(check_out__gte=date_from)
        )

        serializer = StaySerializer(stays, many=True)
        return Response(serializer.data)

    # 🔥 Кто убирал номер клиента
    @extend_schema(
        parameters=[
            OpenApiParameter(name='guest', type=int, required=True),
            OpenApiParameter(name='weekday', type=int, required=True),
        ]
    )
    @action(detail=False, methods=['get'])
    def cleaner(self, request):
        guest_id = request.query_params.get('guest')
        weekday = request.query_params.get('weekday')

        if not guest_id or not weekday:
            return Response({"error": "guest and weekday are required"}, status=400)

        try:
            weekday = int(weekday)
        except ValueError:
            return Response({"error": "weekday must be int"}, status=400)

        stay = Stay.objects.filter(
            guest_id=guest_id,
            check_out__isnull=True
        ).select_related('room', 'guest').first()

        if not stay:
            return Response({"error": "Guest not staying now"}, status=404)

        floor = stay.room.floor

        schedules = CleaningSchedule.objects.filter(
            floor=floor,
            weekday=weekday
        ).select_related('staff')

        if not schedules.exists():
            return Response({"message": "No cleaning scheduled for this floor/day"}, status=200)

        return Response({
            "guest_id": stay.guest_id,
            "room_number": stay.room.number,
            "floor": floor,
            "weekday": weekday,
            "cleaners": [
                f"{s.staff.last_name} {s.staff.first_name}" for s in schedules
            ]
        })

    # 🔥 Пересекающиеся клиенты
    @action(detail=False, methods=['get'])
    def overlapping(self, request):
        passport = request.query_params.get('passport')

        stay = Stay.objects.filter(
            guest__passport_number=passport
        ).first()

        if not stay:
            return Response({"error": "Stay not found"}, status=400)

        overlaps = Stay.objects.filter(
            check_in__lte=stay.check_out
        ).filter(
            Q(check_out__gte=stay.check_in)
        ).exclude(guest=stay.guest)

        serializer = StaySerializer(overlaps, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='guest', type=int, required=True),
        ]
    )
    @action(detail=False, methods=['get'])
    def overlaps(self, request):

        guest_id = request.query_params.get('guest')

        if not guest_id:
            return Response({"error": "guest required"}, status=400)

        stay = Stay.objects.filter(guest_id=guest_id).first()

        if not stay:
            return Response({"error": "stay not found"}, status=404)

        overlapping = Stay.objects.filter(
            check_in__lt=stay.check_out,
            check_out__gt=stay.check_in
        ).exclude(guest_id=guest_id)

        return Response({
            "guest": guest_id,
            "overlapping_guests": [
                s.guest.full_name for s in overlapping
            ]
        })


# =========================
# STAFF
# =========================

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


# =========================
# CLEANING SCHEDULE
# =========================

class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer


# =========================
# QUARTER REPORT 🔥🔥🔥
# =========================

class QuarterReportAPIView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name='year', type=int, required=True),
            OpenApiParameter(name='quarter', type=int, required=True),
        ]
    )

    def get(self, request):

        year = request.query_params.get("year")
        quarter = request.query_params.get("quarter")

        if not year or not quarter:
            return Response({"error": "year and quarter required"}, status=400)

        year = int(year)
        quarter = int(quarter)

        start_month = (quarter - 1) * 3 + 1
        start_date = date(year, start_month, 1)

        if quarter == 4:
            end_date = date(year, 12, 31)
        else:
            end_date = date(year, start_month + 3, 1)

        stays = Stay.objects.filter(check_in__lte=end_date).filter(
            Q(check_out__isnull=True) | Q(check_out__gte=start_date)
        )

        income_by_room = {}
        total_income = 0

        for stay in stays:
            days_delta = (stay.check_out or date.today()) - stay.check_in
            days = days_delta.days

            income = days * float(stay.room.price_per_day)

            income_by_room.setdefault(stay.room.number, 0)
            income_by_room[stay.room.number] += income
            total_income += income

        return Response({
            "income_by_room": income_by_room,
            "total_income": total_income
        })









