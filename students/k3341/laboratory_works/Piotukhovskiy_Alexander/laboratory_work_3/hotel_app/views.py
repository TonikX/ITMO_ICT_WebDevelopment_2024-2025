import calendar
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError as DRFValidationError
from django.db import transaction
from django.db.models import Q, Sum, Count, F, ExpressionWrapper, IntegerField
from django.db.models.functions import Cast, Substr
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Reservation, Client, Room, CleaningSchedule, Employee, EmployeePosition, EmploymentContract, \
    RoomPriceHistory
from .serializers import ClientSerializer, RoomSerializer, ClientStayOverlapSerializer, CleaningEmployeeSerializer, \
    ClientRoomCleaningSerializer, HireEmployeeSerializer, FireEmployeeSerializer, EmploymentContractDetailSerializer, \
    UpdateEmployeeSerializer, UpdateCleaningScheduleSerializer, CreateReservationSerializer, \
    UpdateReservationSerializer, QuarterlyReportSerializer, ReservationSerializer, EmployeeSerializer, \
    CleaningScheduleSerializer, EmployeePositionSerializer


class PublicEndpoint(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Hello GET world!"})

    def post(self, request):
        return Response({"message": "Hello POST world!"})


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmploymentContractViewSet(viewsets.ModelViewSet):
    queryset = EmploymentContract.objects.all()
    serializer_class = EmploymentContractDetailSerializer


class EmployeePositionsViewSet(viewsets.ModelViewSet):
    queryset = EmployeePosition.objects.all()
    serializer_class = EmployeePositionSerializer


class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer


class ClientsListView(generics.ListAPIView):
    serializer_class = ClientSerializer

    def get_queryset(self):
        room_number = self.request.query_params.get('room', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        city_name = self.request.query_params.get('city', None)

        queryset = Client.objects.all()

        if room_number:
            try:
                room_number = Room.objects.get(number=room_number)
            except Room.DoesNotExist:
                return Client.objects.none()

            reservations = Reservation.objects.filter(room=room_number)
            client_ids = reservations.values_list('client_id', flat=True)
            queryset = queryset.filter(id__in=client_ids)

        if start_date or end_date:
            date_filter = Q()

            if start_date:
                date_filter &= Q(departure_date__gte=start_date)

            if end_date:
                date_filter &= Q(arrival_date__lte=end_date)

            reservations = Reservation.objects.filter(date_filter)
            client_ids = reservations.values_list('client_id', flat=True)
            queryset = queryset.filter(id__in=client_ids)

        if city_name:
            queryset = queryset.filter(city_from__icontains=city_name)

        return queryset

    @swagger_auto_schema(
        operation_description="Получить список клиентов с возможностью фильтрации по номеру комнаты, датам проживания и городу.",
        manual_parameters=[
            openapi.Parameter(
                'room',
                openapi.IN_QUERY,
                description="Номер комнаты для фильтрации. Возвращаются клиенты, проживавшие в указанной комнате.",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Дата начала проживания (формат YYYY-MM-DD). Возвращаются клиенты, которые проживали начиная с этой даты.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=False,
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="Дата окончания проживания (формат YYYY-MM-DD). Возвращаются клиенты, которые проживали до этой даты.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=False,
            ),
            openapi.Parameter(
                'city',
                openapi.IN_QUERY,
                description="Город, из которого приехал клиент. Фильтрация клиентов по городу.",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Список клиентов, соответствующих критериям фильтрации.",
                examples={
                    "application/json": {
                        "count": 2,
                        "clients": [
                            {
                                "id": 1,
                                "passport_number": "1234567890",
                                "first_name": "Иван",
                                "last_name": "Иванов",
                                "middle_name": "Иванович",
                                "city_from": "Москва"
                            },
                            {
                                "id": 2,
                                "passport_number": "0987654321",
                                "first_name": "Анна",
                                "last_name": "Петрова",
                                "middle_name": "Александровна",
                                "city_from": "Санкт-Петербург"
                            }
                        ]
                    }
                },
            ),
            404: openapi.Response(
                description="Клиенты не найдены по указанным критериям фильтрации.",
                examples={
                    "application/json": {
                        "detail": "Не найдено ни одного клиента по заданным фильтрам.",
                        "count": 0,
                        "clients": []
                    }
                },
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        clients_count = queryset.count()

        if clients_count > 0:
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "count": clients_count,
                "clients": serializer.data
            })
        else:
            return Response({
                "detail": "Не найдено ни одного клиента по заданным фильтрам.",
                "count": clients_count,
                "clients": []
            }, status=404)


class RoomsByStatusView(generics.GenericAPIView):

    @swagger_auto_schema(
        operation_description="Получить список комнат по их статусам. Возвращает комнаты с указанными статусами и общее их количество.",
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Список статусов комнат через запятую. Доступные значения: ['AVAILABLE', 'OCCUPIED', 'REQUIRES_CLEANING', 'CLEANING_IN_PROGRESS', 'MAINTENANCE'].",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Список комнат с указанными статусами.",
                examples={
                    "application/json": {
                        "count": 3,
                        "rooms": [
                            {
                                "number": 101,
                                "type_id": 1,
                                "type_name": "Одноместный",
                                "phone": "1234567890",
                                "current_client": {
                                    "id": 2,
                                    "passport_number": "0987654321",
                                    "first_name": "Анна",
                                    "last_name": "Смирнова",
                                    "middle_name": None,
                                    "city_from": "Москва"
                                }
                            },
                            {
                                "number": 102,
                                "type_id": 1,
                                "type_name": "Одноместный",
                                "phone": "1234567891",
                                "current_client": None,
                            },
                            {
                                "number": 201,
                                "type_id": 2,
                                "type_name": "Двухместный",
                                "phone": "1234567892"
                            }
                        ]
                    }
                },
            ),
            422: openapi.Response(
                description="Ошибки валидации. Например, отсутствует обязательный параметр или указаны недопустимые статусы.",
                examples={
                    "application/json": {
                        "detail": "Параметр 'status' обязателен для этого запроса."
                    },
                    "application/json_invalid": {
                        "detail": "Недопустимые статусы: ['INVALID_STATUS']. Доступные статусы: ['AVAILABLE', 'OCCUPIED', 'REQUIRES_CLEANING', 'CLEANING_IN_PROGRESS', 'MAINTENANCE']."
                    }
                },
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        statuses = request.query_params.get('status', None)
        rooms_queryset = Room.objects.all()
        if statuses:
            status_list = [status.strip().upper() for status in statuses.split(',') if status.strip()]
            valid_statuses = [choice[0] for choice in Room.STATUS_CHOICES]
            invalid_statuses = [status for status in status_list if status not in valid_statuses]
            if invalid_statuses:
                return Response(
                    {"detail": f"Недопустимые статусы: {invalid_statuses}. Доступные статусы: {valid_statuses}"},
                    status=422
                )
            rooms_queryset = rooms_queryset.filter(status__in=status_list)
        rooms_count = rooms_queryset.count()
        rooms_data = RoomSerializer(rooms_queryset, many=True).data

        return Response({
            "count": rooms_count,
            "rooms": rooms_data
        })


class ClientStayOverlapView(generics.GenericAPIView):
    serializer_class = ClientStayOverlapSerializer

    @swagger_auto_schema(
        operation_description="Получить список клиентов, проживавших в те же дни, что и заданный клиент, в определённый период времени.",
        manual_parameters=[
            openapi.Parameter(
                'client_id',
                openapi.IN_QUERY,
                description="ID клиента, для которого ищутся пересекающиеся проживания.",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Дата начала периода (формат YYYY-MM-DD). Указывается для фильтрации пересечений.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=False,
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="Дата окончания периода (формат YYYY-MM-DD). Указывается для фильтрации пересечений.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                required=False,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Список клиентов, проживавших в те же дни, что и указанный клиент, в заданный период.",
                examples={
                    "application/json": {
                        "count": 2,
                        "clients": [
                            {
                                "id": 1,
                                "passport_number": "1234567890",
                                "first_name": "Иван",
                                "last_name": "Иванов",
                                "middle_name": "Иванович",
                                "city_from": "Москва"
                            },
                            {
                                "id": 2,
                                "passport_number": "0987654321",
                                "first_name": "Анна",
                                "last_name": "Петрова",
                                "middle_name": "Александровна",
                                "city_from": "Санкт-Петербург"
                            }
                        ]
                    }
                },
            ),
            404: openapi.Response(
                description="Клиент с указанным ID не найден или отсутствуют пересечения проживания.",
                examples={
                    "application/json": {
                        "detail": "Клиент с id 123 не найден.",
                        "count": 0,
                        "clients": []
                    }
                },
            ),
            422: openapi.Response(
                description="Ошибки валидации данных. Например, указаны некорректные даты или отсутствует обязательный параметр.",
                examples={
                    "application/json": {
                        "detail": "Дата окончания не может быть раньше даты начала."
                    }
                },
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        overlap_serializer = self.get_serializer(data=request.query_params)
        if not overlap_serializer.is_valid():
            return Response(overlap_serializer.errors, status=422)

        validated_data = overlap_serializer.validated_data
        client_id = validated_data['client_id']
        start_date = validated_data.get('start_date', None)
        end_date = validated_data.get('end_date', None)

        try:
            target_client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response(
                {"detail": f"Клиент с id {client_id} не найден."},
                status=404
            )

        client_reservations = Reservation.objects.filter(client=target_client)

        date_filter = Q()
        if start_date:
            date_filter &= Q(arrival_date__gte=start_date)
        if end_date:
            date_filter &= Q(departure_date__lte=end_date)

        if date_filter:
            client_reservations = client_reservations.filter(date_filter)

        overlapping_filter = Q()
        for reservation in client_reservations:
            overlapping_filter |= Q(arrival_date__lt=reservation.departure_date) & Q(
                departure_date__gt=reservation.arrival_date)

        if overlapping_filter:
            overlapping_reservations = Reservation.objects.filter(overlapping_filter).exclude(client=target_client)
            overlapping_clients_ids = overlapping_reservations.values_list('client_id', flat=True).distinct()
            overlapping_clients = Client.objects.filter(id__in=overlapping_clients_ids)
        else:
            overlapping_clients = Client.objects.none()

        clients_data = ClientSerializer(overlapping_clients, many=True).data

        return Response({
            "count": overlapping_clients.count(),
            "clients": clients_data
        })


class ClientRoomCleaningView(generics.GenericAPIView):
    serializer_class = ClientRoomCleaningSerializer

    @swagger_auto_schema(
        operation_description="Получить список сотрудников, убирающих номер указанного клиента в заданный день недели.",
        manual_parameters=[
            openapi.Parameter(
                'client_id',
                openapi.IN_QUERY,
                description="ID клиента, чей номер нужно проверить на уборку.",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                'day_of_week',
                openapi.IN_QUERY,
                description=(
                        "День недели, когда требуется проверить уборку. "
                        "Допустимые значения: ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']."
                ),
                type=openapi.TYPE_STRING,
                enum=['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'],
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Список сотрудников, убирающих номер клиента в указанный день недели.",
                examples={
                    "application/json": {
                        "count": 2,
                        "employees": [
                            {
                                "id": 1,
                                "first_name": "Иван",
                                "last_name": "Иванов",
                                "middle_name": "Иванович"
                            },
                            {
                                "id": 2,
                                "first_name": "Анна",
                                "last_name": "Петрова",
                                "middle_name": None
                            }
                        ]
                    }
                },
            ),
            404: openapi.Response(
                description="Клиент или уборочные записи для указанного дня не найдены.",
                examples={
                    "application/json": {
                        "detail": "Клиент с id 123 не найден."
                    }
                },
            ),
            422: openapi.Response(
                description="Ошибки валидации данных. Например, указаны некорректные параметры или их недостаточно.",
                examples={
                    "application/json": {
                        "detail": "Недопустимое значение для 'day_of_week'. Допустимые значения: ['MONDAY', 'TUESDAY', ...]."
                    }
                },
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        cleaning_serializer = self.get_serializer(data=request.query_params)
        if not cleaning_serializer.is_valid():
            return Response(cleaning_serializer.errors, status=422)

        validated_data = cleaning_serializer.validated_data
        client_id = validated_data['client_id']
        day_of_week = validated_data['day_of_week']

        try:
            target_client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response(
                {"detail": f"Клиент с id {client_id} не найден."},
                status=404
            )

        try:
            reservation = Reservation.objects.filter(client=target_client).latest('departure_date')
            room = reservation.room
        except Reservation.DoesNotExist:
            return Response(
                {"detail": f"Нет активных или завершённых бронирований для клиента с id {client_id}."},
                status=404
            )

        cleaning_schedules = CleaningSchedule.objects.filter(
            room=room,
            cleaning_date__week_day=self.get_day_number(day_of_week)
        )

        employees = [schedule.cleaner.employee for schedule in cleaning_schedules]
        employees_data = CleaningEmployeeSerializer(employees, many=True).data

        return Response({
            "count": len(employees),
            "employees": employees_data
        })

    def get_day_number(self, day_of_week):
        days = {
            'MONDAY': 2,
            'TUESDAY': 3,
            'WEDNESDAY': 4,
            'THURSDAY': 5,
            'FRIDAY': 6,
            'SATURDAY': 7,
            'SUNDAY': 1,
        }
        return days.get(day_of_week.upper(), None)


class EmployeeManagementView(generics.GenericAPIView):
    serializer_classes = {
        'post': HireEmployeeSerializer,
        'delete': FireEmployeeSerializer,
        'patch': UpdateEmployeeSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method.lower())

    @swagger_auto_schema(
        operation_description="Принять на работу нового сотрудника гостиницы. Создание сотрудника и контракта.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'passport_number': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Номер паспорта сотрудника (уникальный).",
                ),
                'first_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Имя сотрудника.",
                ),
                'last_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Фамилия сотрудника.",
                ),
                'middle_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Отчество сотрудника (необязательно).",
                    nullable=True,
                ),
                'position_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID должности для нового сотрудника.",
                ),
                'contract_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['FIXED_TERM', 'PERMANENT', 'CIVIL_CONTRACT'],
                    description="Тип контракта: FIXED_TERM (срочный), PERMANENT (бессрочный), CIVIL_CONTRACT (гражданский договор).",
                ),
                'start_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATE,
                    description="Дата начала контракта (формат YYYY-MM-DD).",
                ),
                'end_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATE,
                    description="Дата окончания контракта (необязательна для PERMANENT).",
                    nullable=True,
                ),
            },
            required=['passport_number', 'first_name', 'last_name', 'position_id', 'contract_type', 'start_date'],
        ),
        responses={
            201: openapi.Response(
                description="Сотрудник успешно добавлен и контракт создан.",
                examples={
                    "application/json": {
                        "id": 1,
                        "contract_type": "FIXED_TERM",
                        "employee_id": 10,
                        "employee_first_name": "Иван",
                        "employee_last_name": "Иванов",
                        "employee_middle_name": "Иванович",
                        "start_date": "2024-01-01",
                        "end_date": "2025-01-01",
                        "position_id": 2,
                        "position_name": "Уборщик"
                    }
                },
            ),
            422: openapi.Response(
                description="Ошибки валидации данных. Например, указаны некорректные данные или сотрудник уже существует.",
                examples={
                    "application/json": {
                        "detail": "У сотрудника уже есть активный контракт."
                    }
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            passport_number = validated_data['passport_number']

            employee, created = Employee.objects.get_or_create(
                passport_number=passport_number,
                defaults={
                    "first_name": validated_data['first_name'],
                    "last_name": validated_data['last_name'],
                    "middle_name": validated_data.get('middle_name', None)
                }
            )

            if not created:
                employee.first_name = validated_data['first_name']
                employee.last_name = validated_data['last_name']
                employee.middle_name = validated_data.get('middle_name', None)
                employee.save()

            if EmploymentContract.objects.filter(employee=employee, is_active=True).exists():
                return Response(
                    {"detail": "У сотрудника уже есть активный контракт."},
                    status=422
                )
            position = EmployeePosition.objects.get(id=validated_data['position_id'])
            contract = EmploymentContract.objects.create(
                employee=employee,
                position=position,
                contract_type=validated_data['contract_type'],
                start_date=validated_data['start_date'],
                end_date=validated_data.get('end_date')
            )

            contract_serializer = EmploymentContractDetailSerializer(contract)
            return Response(contract_serializer.data, status=201)

        return Response(serializer.errors, status=422)

    @swagger_auto_schema(
        operation_description="Обновить данные сотрудника или его контракта.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'employee_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID сотрудника, данные которого нужно обновить.",
                ),
                'first_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Новое имя сотрудника (необязательно).",
                    nullable=True,
                ),
                'last_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Новая фамилия сотрудника (необязательно).",
                    nullable=True,
                ),
                'middle_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Новое отчество сотрудника (необязательно).",
                    nullable=True,
                ),
                'passport_number': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Новый номер паспорта сотрудника (необязательно).",
                    nullable=True,
                ),
                'position_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID новой должности сотрудника (необязательно).",
                    nullable=True,
                ),
                'contract_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['FIXED_TERM', 'PERMANENT', 'CIVIL_CONTRACT'],
                    description="Новый тип контракта: FIXED_TERM, PERMANENT, CIVIL_CONTRACT (необязательно).",
                    nullable=True,
                ),
                'start_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATE,
                    description="Новая дата начала контракта (необязательно).",
                    nullable=True,
                ),
                'end_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATE,
                    description="Новая дата окончания контракта (необязательно).",
                    nullable=True,
                ),
            },
            required=['employee_id'],
        ),
        responses={
            200: openapi.Response(
                description="Данные сотрудника или его контракта успешно обновлены.",
                examples={
                    "application/json": {
                        "id": 1,
                        "contract_type": "FIXED_TERM",
                        "employee_id": 10,
                        "employee_first_name": "Иван",
                        "employee_last_name": "Иванов",
                        "employee_middle_name": "Иванович",
                        "start_date": "2024-01-01",
                        "end_date": "2025-01-01",
                        "position_id": 2,
                        "position_name": "Уборщик"
                    }
                },
            ),
            422: openapi.Response(
                description="Ошибки валидации данных. Например, указан несуществующий сотрудник или недопустимая дата.",
                examples={
                    "application/json": {
                        "detail": "Активный контракт для указанного сотрудника не найден."
                    }
                },
            ),
        },
    )
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            employee_id = validated_data['employee_id']

            with transaction.atomic():
                employee = Employee.objects.select_for_update().get(id=employee_id)

                employee.first_name = validated_data.get('first_name', employee.first_name)
                employee.last_name = validated_data.get('last_name', employee.last_name)
                employee.middle_name = validated_data.get('middle_name', employee.middle_name)
                employee.passport_number = validated_data.get('passport_number', employee.passport_number)
                employee.save()

                new_position_id = validated_data.get('position_id')
                new_contract_type = validated_data.get('contract_type')
                new_start_date = validated_data.get('start_date', timezone.now())
                new_end_date = validated_data.get('end_date')

                if new_position_id or new_contract_type:
                    try:
                        old_contract = EmploymentContract.objects.select_for_update().get(employee=employee,
                                                                                          is_active=True)
                        old_contract.terminate_contract(termination_date=new_start_date)
                    except EmploymentContract.DoesNotExist:
                        raise DRFValidationError("Активный контракт для указанного сотрудника не найден.")

                    position = EmployeePosition.objects.get(id=new_position_id)
                    new_contract = EmploymentContract.objects.create(
                        employee=employee,
                        position=position,
                        contract_type=new_contract_type,
                        start_date=new_start_date,
                        end_date=new_end_date
                    )
                    contract_serializer = EmploymentContractDetailSerializer(new_contract)
                    return Response(contract_serializer.data)

                active_contract = EmploymentContract.objects.filter(employee=employee, is_active=True).first()
                if not active_contract:
                    raise DRFValidationError(
                        "Активный контракт не найден, несмотря на успешную попытку обновления данных.")

                contract_serializer = EmploymentContractDetailSerializer(active_contract)
                return Response(contract_serializer.data, status=200)

        return Response(serializer.errors, status=422)

    @swagger_auto_schema(
        operation_description="Уволить сотрудника, завершив его активный контракт.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'employee_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID сотрудника, которого нужно уволить.",
                ),
                'termination_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATE,
                    description="Дата увольнения (по умолчанию текущая дата).",
                    nullable=True,
                ),
            },
            required=['employee_id'],
        ),
        responses={
            200: openapi.Response(
                description="Контракт сотрудника успешно завершён.",
                examples={
                    "application/json": {
                        "detail": "Активный контракт сотрудника успешно завершен."
                    }
                },
            ),
            422: openapi.Response(
                description="Ошибки валидации данных. Например, указан несуществующий сотрудник или сотрудник не имеет активного контракта.",
                examples={
                    "application/json": {
                        "detail": "Активный контракт для указанного сотрудника не найден."
                    }
                },
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            employee_id = validated_data['employee_id']
            termination_date = validated_data.get('termination_date', timezone.now())

            try:
                contract = EmploymentContract.objects.get(employee_id=employee_id, is_active=True)
            except EmploymentContract.DoesNotExist:
                return Response(
                    {"detail": "Активный контракт для указанного сотрудника не найден."},
                    status=422
                )

            contract.terminate_contract(termination_date=termination_date)
            return Response({"detail": "Активный контракт сотрудника успешно завершен."})

        return Response(serializer.errors, status=422)


class CleaningScheduleManagementView(generics.GenericAPIView):
    serializer_class = UpdateCleaningScheduleSerializer

    @swagger_auto_schema(
        operation_description="Обновить расписание уборок для сотрудника.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'cleaner_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID сотрудника (уборщика), для которого обновляется расписание.",
                ),
                'cleaning_dates': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                    description="Список дат уборки (формат YYYY-MM-DD).",
                ),
                'room_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="Список ID комнат, которые сотрудник будет убирать.",
                ),
            },
            required=['cleaner_id', 'cleaning_dates', 'room_ids'],
        ),
        responses={
            200: openapi.Response(
                description="Расписание уборок успешно обновлено.",
                examples={
                    "application/json": {
                        "detail": "Расписание успешно обновлено."
                    }
                },
            ),
            422: openapi.Response(
                description="Ошибки валидации данных. Например, указаны недопустимые комнаты, отсутствующий сотрудник или некорректные даты.",
                examples={
                    "application/json": {
                        "detail": "Указанный служащий не найден или не имеет активного контракта.",
                        "missing_rooms": "Следующие номера комнат не найдены: 101, 102."
                    }
                },
            ),
        },
    )
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            cleaner_id = validated_data['cleaner_id']
            cleaning_dates = validated_data['cleaning_dates']
            room_numbers = validated_data['room_ids']

            with transaction.atomic():
                rooms = Room.objects.filter(number__in=room_numbers)

                CleaningSchedule.objects.filter(
                    cleaner_id=cleaner_id,
                    cleaning_date__in=cleaning_dates,
                    room__in=rooms
                ).delete()

                schedules = [
                    CleaningSchedule(
                        cleaner_id=cleaner_id,
                        room=room,
                        cleaning_date=cleaning_date
                    )
                    for cleaning_date in cleaning_dates
                    for room in rooms
                ]
                CleaningSchedule.objects.bulk_create(schedules)

            return Response({"detail": "Расписание успешно обновлено."})

        return Response(serializer.errors, status=422)


class ReservationManagementView(generics.GenericAPIView):
    serializer_classes = {
        'post': CreateReservationSerializer,
        'patch': UpdateReservationSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method.lower())

    @swagger_auto_schema(
        operation_description="Создать новое бронирование для клиента.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'passport_number': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Номер паспорта клиента (уникальный). Если клиента с таким паспортом не существует, он будет создан.",
                ),
                'first_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Имя клиента. Указывается при создании нового клиента.",
                ),
                'last_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Фамилия клиента. Указывается при создании нового клиента.",
                ),
                'middle_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Отчество клиента (необязательно).",
                    nullable=True,
                ),
                'city_from': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Город, из которого прибыл клиент.",
                ),
                'room_number': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Номер комнаты, в которую заселяется клиент.",
                ),
                'arrival_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATE,
                    description="Дата заселения (формат YYYY-MM-DD).",
                ),
                'departure_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATE,
                    description="Дата выезда (формат YYYY-MM-DD).",
                ),
                'status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['BOOKED', 'CONFIRMED', 'CHECKED_IN', 'CHECKED_OUT', 'CANCELLED'],
                    description="Статус бронирования. По умолчанию BOOKED.",
                    nullable=True,
                ),
                'payment_status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['PREPAID', 'PAID', 'UNPAID', 'REFUNDED'],
                    description="Статус оплаты. По умолчанию UNPAID.",
                    nullable=True,
                ),
            },
            required=['passport_number', 'first_name', 'last_name', 'city_from', 'room_number', 'arrival_date',
                      'departure_date'],
        ),
        responses={
            201: openapi.Response(
                description="Бронирование успешно создано.",
                examples={
                    "application/json": {
                        "reservation_id": 1,
                        "client_id": 10,
                        "room_number": 101,
                        "arrival_date": "2024-12-10",
                        "departure_date": "2024-12-15",
                        "status": "BOOKED",
                        "price_at_booking": 5000
                    }
                },
            ),
            422: openapi.Response(
                description="Ошибки валидации данных. Например, некорректные даты или комната недоступна.",
                examples={
                    "application/json": {
                        "room_number": "Комната с номером 101 не найдена.",
                        "departure_date": "Дата выезда должна быть позже даты заселения."
                    }
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            passport_number = validated_data['passport_number']
            first_name = validated_data['first_name']
            last_name = validated_data['last_name']
            middle_name = validated_data.get('middle_name')
            city_from = validated_data['city_from']
            room = validated_data['room']
            arrival_date = validated_data['arrival_date']
            departure_date = validated_data['departure_date']
            status = request.data.get('status', None)
            payment_status = request.data.get('payment_status', None)

            with transaction.atomic():
                client, created = Client.objects.get_or_create(
                    passport_number=passport_number,
                    defaults={
                        "first_name": first_name,
                        "last_name": last_name,
                        "middle_name": middle_name,
                        "city_from": city_from
                    }
                )

                if not created:
                    client.first_name = first_name
                    client.last_name = last_name
                    client.middle_name = middle_name
                    client.city_from = city_from
                    client.save()

                total_price = self.calculate_total_price(room, arrival_date, departure_date)

                reservation = Reservation.objects.create(
                    client=client,
                    room=room,
                    admin=request.user,
                    booking_date=datetime.now(),
                    arrival_date=arrival_date,
                    departure_date=departure_date,
                    status=status or Reservation._meta.get_field('status').get_default(),
                    payment_status=payment_status or Reservation._meta.get_field('payment_status').get_default(),
                    price_at_booking=total_price,
                    final_price=total_price,
                )

                room.status = 'OCCUPIED'
                room.save()

            return Response(
                {
                    "reservation_id": reservation.id,
                    "client_id": client.id,
                    "room_number": room.number,
                    "arrival_date": reservation.arrival_date,
                    "departure_date": reservation.departure_date,
                    "status": reservation.status,
                    "price_at_booking": reservation.price_at_booking
                },
                status=201
            )

        return Response(serializer.errors, status=422)

    @swagger_auto_schema(
        operation_description="Обновить существующее бронирование.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'arrival_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATE,
                    description="Новая дата заселения (формат YYYY-MM-DD).",
                    nullable=True,
                ),
                'departure_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATE,
                    description="Новая дата выезда (формат YYYY-MM-DD).",
                    nullable=True,
                ),
                'status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['BOOKED', 'CONFIRMED', 'CHECKED_IN', 'CHECKED_OUT', 'CANCELLED'],
                    description="Новый статус бронирования.",
                    nullable=True,
                ),
                'payment_status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['PREPAID', 'PAID', 'UNPAID', 'REFUNDED'],
                    description="Новый статус оплаты.",
                    nullable=True,
                ),
                'room_number': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Новый номер комнаты для бронирования.",
                    nullable=True,
                ),
            },
            required=[],
        ),
        responses={
            200: openapi.Response(
                description="Бронирование успешно обновлено.",
                examples={
                    "application/json": {
                        "reservation_id": 1,
                        "client_id": 10,
                        "room_number": 101,
                        "arrival_date": "2024-12-12",
                        "departure_date": "2024-12-18",
                        "status": "CONFIRMED",
                        "payment_status": "PAID",
                        "price_at_booking": 7000
                    }
                },
            ),
            404: openapi.Response(
                description="Бронирование с указанным ID не найдено.",
                examples={
                    "application/json": {
                        "detail": "Бронирование с указанным ID не найдено."
                    }
                },
            ),
            422: openapi.Response(
                description="Ошибки валидации данных. Например, некорректные даты или комната недоступна.",
                examples={
                    "application/json": {
                        "departure_date": "Дата выезда должна быть позже даты заселения.",
                        "room_number": "Комната с номером 102 недоступна для бронирования."
                    }
                },
            ),
        },
    )
    def patch(self, request, *args, **kwargs):
        reservation_id = kwargs.get('reservation_id')

        try:
            reservation = Reservation.objects.select_for_update().get(id=reservation_id)
        except Reservation.DoesNotExist:
            return Response(
                {"detail": "Бронирование с указанным ID не найдено."},
                status=404
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            with transaction.atomic():
                if 'arrival_date' in validated_data:
                    reservation.arrival_date = validated_data['arrival_date']
                if 'departure_date' in validated_data:
                    reservation.departure_date = validated_data['departure_date']

                previous_status = reservation.status
                if 'status' in validated_data:
                    reservation.status = validated_data['status']

                    if validated_data['status'] in ['CANCELED', 'CHECKED_OUT']:
                        if validated_data['status'] == 'CANCELED' and previous_status != 'CHECKED_IN':
                            reservation.room.status = 'AVAILABLE'
                        elif validated_data['status'] == 'CHECKED_OUT' and previous_status == 'CHECKED_IN':
                            reservation.room.status = 'REQUIRES_CLEANING'
                        reservation.room.save()

                if 'payment_status' in validated_data:
                    reservation.payment_status = validated_data['payment_status']
                if 'room' in validated_data:
                    reservation.room.status = 'AVAILABLE'
                    reservation.room.save()
                    reservation.room = validated_data['room']
                    reservation.room.status = 'OCCUPIED'
                    reservation.room.save()

                if 'arrival_date' in validated_data or 'departure_date' in validated_data or 'room' in validated_data:
                    reservation.price_at_booking = self.calculate_total_price(
                        reservation.room,
                        reservation.arrival_date,
                        reservation.departure_date
                    )

                reservation.updated_by = request.user
                reservation.last_updated_date = timezone.now()
                reservation.save()

            return Response(
                {
                    "reservation_id": reservation.id,
                    "client_id": reservation.client.id,
                    "room_number": reservation.room.number,
                    "arrival_date": reservation.arrival_date,
                    "departure_date": reservation.departure_date,
                    "status": reservation.status,
                    "payment_status": reservation.payment_status,
                    "price_at_booking": reservation.price_at_booking,
                },
                status=200
            )

        return Response(serializer.errors, status=422)

    def calculate_total_price(self, room, arrival_date, departure_date):
        total_price = 0
        current_date = arrival_date

        price_history = RoomPriceHistory.objects.filter(
            room_type=room.type
        ).order_by('start_date')

        while current_date < departure_date:
            for price_period in price_history:
                if price_period.start_date <= current_date and (
                        price_period.end_date is None or price_period.end_date >= current_date):
                    total_price += price_period.price
                    break

            current_date += timedelta(days=1)
        return total_price


class QuarterlyReportView(generics.GenericAPIView):

    @swagger_auto_schema(
        operation_description="Сформировать отчет о работе гостиницы за указанный квартал текущего или прошлого года.",
        manual_parameters=[
            openapi.Parameter(
                'quarter',
                openapi.IN_QUERY,
                description="Номер квартала (1, 2, 3 или 4).",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                'year',
                openapi.IN_QUERY,
                description="Год для отчета. Должен быть текущим или прошлым.",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Успешно сформированный отчет по кварталу.",
                examples={
                    "application/json": {
                        "clients_per_room": [
                            {"room__number": 101, "client_count": 5},
                            {"room__number": 102, "client_count": 3}
                        ],
                        "rooms_per_floor": [
                            {"floor": 1, "room_count": 10},
                            {"floor": 2, "room_count": 8}
                        ],
                        "income_per_room": [
                            {"room__number": 101, "total_income": 15000},
                            {"room__number": 102, "total_income": 12000}
                        ],
                        "total_income": 27000,
                        "start_date": "2024-04-01",
                        "end_date": "2024-06-30"
                    }
                },
            ),
            422: openapi.Response(
                description="Ошибки валидации данных. Например, указаны некорректный год или квартал.",
                examples={
                    "application/json": {
                        "detail": "Год не может быть в будущем.",
                    }
                },
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        serializer = QuarterlyReportSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=422)

        quarter = serializer.validated_data['quarter']
        year = serializer.validated_data['year']

        start_date, end_date = self.get_quarter_date_range(quarter, year)

        # Число клиентов за период в каждом номере
        clients_per_room = (
            Reservation.objects.filter(
                arrival_date__gte=start_date,
                departure_date__lte=end_date,
                status__in=['BOOKED', 'CONFIRMED', 'CHECKED_IN', 'CHECKED_OUT']
            )
            .values('room__number')
            .annotate(client_count=Count('id'))
            .order_by('room__number')
        )

        # Количество номеров на каждом этаже
        rooms_per_floor = (
            Room.objects.annotate(
                floor=ExpressionWrapper(
                    Substr(F('number'), 1, 1),
                    output_field=IntegerField()
                )
            )
            .values('floor')
            .annotate(room_count=Count('id'))
            .order_by('floor')
        )

        # Общая сумма дохода за каждый номер
        income_per_room = (
            Reservation.objects.filter(
                arrival_date__gte=start_date,
                departure_date__lte=end_date,
                payment_status__in=['PREPAID', 'PAID'],
            )
            .values('room__number')
            .annotate(total_income=Sum('price_at_booking'))
            .order_by('room__number')
        )

        # Суммарный доход по всей гостинице
        total_income = (
                           Reservation.objects.filter(
                               arrival_date__gte=start_date,
                               departure_date__lte=end_date,
                               payment_status__in=['PREPAID', 'PAID']
                           )
                           .aggregate(total_income=Sum('price_at_booking'))['total_income']
                       ) or 0

        report = {
            "clients_per_room": list(clients_per_room),
            "rooms_per_floor": list(rooms_per_floor),
            "income_per_room": list(income_per_room),
            "total_income": total_income,
            "start_date": start_date,
            "end_date": end_date
        }

        return Response(report, status=200)

    def get_quarter_date_range(self, quarter, year):
        start_month = (quarter - 1) * 3 + 1
        end_month = start_month + 2

        start_date = datetime(year, start_month, 1)
        last_day = calendar.monthrange(year, end_month)[1]
        end_date = datetime(year, end_month, last_day)

        return start_date, end_date
