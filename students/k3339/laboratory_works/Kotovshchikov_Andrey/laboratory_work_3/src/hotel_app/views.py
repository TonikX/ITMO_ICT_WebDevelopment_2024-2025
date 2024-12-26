import calendar
from datetime import date
from django.db.models import (
    Prefetch,
    Count,
    Sum,
    Value,
    F,
    ExpressionWrapper,
    fields,
    functions,
)


from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import transaction
from django.db import connection
from drf_yasg.utils import swagger_auto_schema

from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from hotel_app import queries
from hotel_project.exceptions import Conflict, BadRequest
from hotel_app.filters import EmployeeFilter, IsRoomAvailableFilterBackend
from hotel_app.models import Booking, Employee, Floor, Guest, Room, Schedule
from hotel_app.pagination import EmployeePagination, GuestPagination, RoomPagination
from hotel_app.serializers import (
    DateRangeSerializer,
    EmployeeDetailSerializer,
    EmployeeSerializer,
    GuestDetailSerializer,
    GuestSerializer,
    RoomBookingSerializer,
    RoomGuestSerializer,
    RoomSerializer,
    ScheduleCreateSerializer,
)


class EmployeeView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer
    pagination_class = EmployeePagination
    queryset = Employee.objects.all().distinct()

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EmployeeFilter
    ordering = ("hire_date",)


class EmployeeDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeDetailSerializer
    queryset = Employee.objects.prefetch_related(
        Prefetch(
            "schedule",
            queryset=Schedule.objects.select_related("floor")
            .all()
            .only("week_day", "floor__number"),
        )
    ).all()

    filter_backends = [filters.OrderingFilter]
    ordering = ("hire_date",)


class EmployeeScheduleCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleCreateSerializer

    def perform_create(self, serializer):
        week_day = serializer.validated_data["week_day"]
        floor_number = serializer.validated_data["floor"]

        employee = generics.get_object_or_404(Employee, id=self.kwargs["employee_pk"])
        if employee.schedule.filter(week_day=week_day).exists():
            raise Conflict("Обнаружено пересечение в расписании")

        floor = Floor.objects.filter(number=floor_number).first()
        if floor is None:
            raise BadRequest("Этаж с таким номером не существует")

        Schedule.objects.create(
            employee=employee,
            floor=floor,
            week_day=week_day,
        )


class EmployeeScheduleResetView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Сбросить расписание сотрудника")
    def delete(self, request: Request, **kwargs):
        employee = generics.get_object_or_404(Employee, id=kwargs["employee_pk"])
        employee.schedule.all().delete()
        return Response(data={"success": "Расписание работника сброшено"})


class GuestView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GuestSerializer
    pagination_class = GuestPagination
    queryset = Guest.objects.all()

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("city",)
    ordering = ("id",)


class GuestDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GuestDetailSerializer
    queryset = Guest.objects.prefetch_related(
        Prefetch(
            "booking",
            queryset=Booking.objects.select_related(
                "room",
                "room__floor",
                "room__room_type",
            )
            .all()
            .order_by("-check_in_date"),
        )
    ).all()


class GuestOverlappingView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        query_serializer=DateRangeSerializer,
        operation_description=(
            "Получить список клиентов с указанием места жительства,"
            "которые проживали в те же дни, что и заданный клиент,"
            "в определенный период времени"
        ),
    )
    def get(self, request: Request, **kwargs):
        serializer = DateRangeSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        start_date = serializer.validated_data.pop("start_date")
        end_date = serializer.validated_data.pop("end_date")

        target_guest = generics.get_object_or_404(
            Guest.objects.prefetch_related(
                Prefetch(
                    "booking",
                    queryset=Booking.objects.filter(
                        check_in_date__lte=end_date,
                        check_out_date__gt=start_date,
                    ),
                )
            ),
            id=kwargs["pk"],
        )

        overlapping_guests_set = set()
        for booking in target_guest.booking.all():
            overlapping_guests = Guest.objects.filter(
                city=target_guest.city,
                booking__check_in_date__lt=booking.check_out_date,
                booking__check_out_date__gt=booking.check_in_date,
            ).exclude(id=target_guest.id)

            overlapping_guests_set.update(overlapping_guests)

        serializer = GuestSerializer(overlapping_guests_set, many=True)
        return Response(data=serializer.data)


class RoomView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer
    pagination_class = RoomPagination
    queryset = Room.objects.select_related("room_type", "floor").all().order_by("id")
    filter_backends = [IsRoomAvailableFilterBackend]


class RoomGuestView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        query_serializer=DateRangeSerializer,
        operation_description="Получить клиентов, проживавших в заданном номере, в заданный период времени",
    )
    def get(self, request: Request, **kwargs):
        serializer = DateRangeSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        start_date = serializer.validated_data.pop("start_date")
        end_date = serializer.validated_data.pop("end_date")

        room = generics.get_object_or_404(
            Room.objects.prefetch_related(
                Prefetch(
                    "guests",
                    queryset=Guest.objects.filter(
                        booking__check_out_date__gt=start_date,
                        booking__check_in_date__lte=end_date,
                    ).distinct(),
                )
            ),
            id=kwargs["pk"],
        )

        return Response(data=RoomGuestSerializer(room).data)


class RoomBookingView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=RoomBookingSerializer,
        operation_description="Забронировать номер для пользователя на текущую дату",
    )
    @transaction.atomic
    def post(self, request: Request, **kwargs):
        serializer = RoomBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        guest_passport = serializer.validated_data.pop("guest_passport")
        check_out_date = serializer.validated_data.pop("check_out_date")

        guest = Guest.objects.filter(passport=guest_passport).first()
        if guest is None:
            raise BadRequest("Гость с таким паспортом не найден")

        room = generics.get_object_or_404(
            Room.objects.select_for_update(no_key=True),
            id=kwargs["pk"],
        )

        is_room_available = not (
            Booking.objects.filter(
                room=room,
                check_in_date__lt=check_out_date,
                check_out_date__gt=timezone.now(),
            ).exists()
        )

        if not is_room_available:
            raise Conflict("Гостиничный номер занят")

        Booking.objects.create(room=room, guest=guest, check_out_date=check_out_date)
        return Response(data={"success": "Номер успешно забронирован"})

    @swagger_auto_schema(
        operation_description="Освободить номер и выселить клиента, который забронировал этот номер на текущую дату",
    )
    def delete(self, request: Request, **kwargs):
        room = generics.get_object_or_404(Room, id=kwargs["pk"])
        actual_booking = (
            Booking.objects.filter(
                room=room,
                check_in_date__lte=timezone.now(),
                check_out_date__gt=timezone.now(),
            )
            .order_by("-check_in_date")
            .first()
        )

        if actual_booking is not None:
            actual_booking.check_out_date = timezone.now()
            actual_booking.save()

        return Response(data={"success": "Гостиничный номер успешно освобожден"})


class ReportPerQuarterView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description=(
            "Сформировать отчет за указанный квартал текущего года:\n"
            "1. число клиентов за указанный период в каждом номере;\n"
            "2. количество номеров не каждом этаже;\n"
            "3. общая сумма дохода за каждый номер;\n"
            "4. суммарный доход по всей гостинице\n"
        ),
    )
    def get(self, request: Request, **kwargs):
        quarter = self.kwargs["quarter"]
        if not (1 <= quarter <= 4):
            raise BadRequest("Квартал должен принимать значения от 1 до 4 включительно")

        current_year = timezone.now().year
        quarter_start_month = 3 * (quarter - 1) + 1
        quarter_end_month = 3 * quarter

        quarter_start = date(
            year=current_year,
            month=quarter_start_month,
            day=1,
        )

        quarter_end = date(
            year=current_year,
            month=quarter_end_month,
            day=calendar.monthrange(current_year, quarter_end_month)[1],
        )

        report = {
            "guests_per_room": self._get_guests_per_room(quarter_start, quarter_end),
            "rooms_per_floor": self._get_rooms_per_floor(),
            "profit_per_room": self._get_profit_per_room(quarter_start, quarter_end),
            "total_profit": self._calculate_total_profit(quarter_start, quarter_end),
        }

        return Response(data=report)

    def _get_guests_per_room(
        self,
        quarter_start: date,
        quarter_end: date,
    ) -> dict:
        booking_per_quarter = (
            Booking.objects.select_related("room")
            .filter(
                check_out_date__gt=quarter_start,
                check_in_date__lte=quarter_end,
            )
            .annotate(guest_count=Count("guest"))
        )

        guests_per_room = dict()
        for booking in booking_per_quarter:
            guests_per_room[booking.room.label] = booking.guest_count

        return guests_per_room

    def _get_rooms_per_floor(self) -> dict:
        rooms_per_floor = dict()
        for floor in Floor.objects.annotate(room_count=Count("rooms")):
            rooms_per_floor[floor.number] = floor.room_count

        return rooms_per_floor

    def _get_profit_per_room(
        self,
        quarter_start: date,
        quarter_end: date,
    ) -> dict:
        profit_per_room = dict()
        with connection.cursor() as cursor:
            cursor.execute(
                queries.SELECT_PROFIT_PER_ROOM_FOR_QUARTER,
                {"quarter_start": quarter_start, "quarter_end": quarter_end},
            )

            rows = cursor.fetchall()
            for row in rows:
                profit_per_room[row[1]] = row[2]

        return profit_per_room

    def _calculate_total_profit(
        self,
        quarter_start: date,
        quarter_end: date,
    ) -> int:
        return (
            Booking.objects.filter(
                check_out_date__gt=quarter_start,
                check_in_date__lte=quarter_end,
            )
            .values("room__label")
            .annotate(
                profit=ExpressionWrapper(
                    functions.ExtractDay(
                        functions.Least(
                            F("check_out_date"),
                            Value(quarter_end + timezone.timedelta(days=1)),
                        )  # + 1 day because last month day is needing to pay
                        - functions.Greatest(
                            F("check_in_date"),
                            Value(quarter_start),
                        )
                    )
                    * F("room__room_type__price_per_day"),
                    output_field=fields.DecimalField(),
                ),
            )
            .aggregate(result=Sum("profit"))["result"]
        ) or 0
