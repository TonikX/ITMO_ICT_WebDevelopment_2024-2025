from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from datetime import date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Room, Client, Stay, Staff, CleaningSchedule
from .serializers import RoomSerializer, ClientSerializer, StaySerializer, StaffSerializer, CleaningScheduleSerializer


class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'floor']


class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city']


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class StayList(generics.ListCreateAPIView):
    queryset = Stay.objects.all()
    serializer_class = StaySerializer


class StayDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stay.objects.all()
    serializer_class = StaySerializer


class StaffList(generics.ListCreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StaffDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class CleaningScheduleList(generics.ListCreateAPIView):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['floor', 'day']


class FreeRoomsView(APIView):
    @swagger_auto_schema(
        operation_description="Получить количество свободных номеров на текущую дату",
        responses={200: openapi.Response('Количество свободных номеров', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'free_rooms': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество')
            }
        ))}
    )
    def get(self, request):
        today = date.today()
        occupied_room_ids = Stay.objects.filter(
            check_in__lte=today,
            check_out__gt=today
        ).values_list('room_id', flat=True)

        free_count = Room.objects.exclude(id__in=occupied_room_ids).count()
        return Response({'free_rooms': free_count})


class ClientsInRoomView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить список клиентов, проживавших в заданном номере за период",
        manual_parameters=[
            openapi.Parameter('room_number', openapi.IN_QUERY, description="Номер комнаты", type=openapi.TYPE_INTEGER,
                              required=True),
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Дата начала (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Дата окончания (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING, required=True),
        ],
        responses={200: StaySerializer(many=True), 400: 'Некорректные параметры'}
    )
    def get(self, request):
        room_number = request.query_params.get('room_number')
        start = request.query_params.get('start_date')
        end = request.query_params.get('end_date')

        if not all([room_number, start, end]):
            return Response(
                {'error': 'Требуются параметры: room_number, start_date, end_date'},
                status=status.HTTP_400_BAD_REQUEST
            )

        stays = Stay.objects.filter(
            room__number=room_number,
            check_in__lte=end,
            check_out__gte=start
        ).select_related('client', 'room')

        serializer = StaySerializer(stays, many=True)
        return Response(serializer.data)


class ClientsFromCityView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить количество клиентов из заданного города",
        manual_parameters=[
            openapi.Parameter('city', openapi.IN_QUERY, description="Название города", type=openapi.TYPE_STRING,
                              required=True),
        ],
        responses={200: openapi.Response('Количество клиентов', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'city': openapi.Schema(type=openapi.TYPE_STRING),
                'count': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ))}
    )
    def get(self, request):
        city = request.query_params.get('city')

        if not city:
            return Response(
                {'error': 'Требуется параметр city'},
                status=status.HTTP_400_BAD_REQUEST
            )

        count = Client.objects.filter(
            stay__isnull=False,
            city=city
        ).distinct().count()

        return Response({'city': city, 'count': count})


class StaffForClientDayView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить список служащих, убиравших номер клиента в заданный день",
        manual_parameters=[
            openapi.Parameter('passport', openapi.IN_QUERY, description="Номер паспорта клиента",
                              type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('day', openapi.IN_QUERY, description="День недели (mon, tue, wed, thu, fri, sat, sun)",
                              type=openapi.TYPE_STRING, required=True),
        ],
        responses={200: CleaningScheduleSerializer(many=True), 404: 'Клиент не найден'}
    )
    def get(self, request):
        passport = request.query_params.get('passport')
        day = request.query_params.get('day')

        if not all([passport, day]):
            return Response(
                {'error': 'Требуются параметры: passport, day'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            stay = Stay.objects.filter(client__passport=passport).first()
            if not stay:
                return Response(
                    {'error': 'Клиент не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )

            schedules = CleaningSchedule.objects.filter(
                floor=stay.room.floor,
                day=day
            ).select_related('staff')

            serializer = CleaningScheduleSerializer(schedules, many=True)
            return Response(serializer.data)

        except Client.DoesNotExist:
            return Response(
                {'error': 'Клиент не найден'},
                status=status.HTTP_404_NOT_FOUND
            )


class QuarterlyReportView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить отчет о работе гостиницы за указанный квартал",
        responses={200: openapi.Response('Квартальный отчет', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'quarter': openapi.Schema(type=openapi.TYPE_INTEGER),
                'year': openapi.Schema(type=openapi.TYPE_INTEGER),
                'period': openapi.Schema(type=openapi.TYPE_STRING),
                'clients_per_room': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                   items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                'rooms_per_floor': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                  items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                'income_per_room': openapi.Schema(type=openapi.TYPE_OBJECT),
                'total_income': openapi.Schema(type=openapi.TYPE_NUMBER)
            }
        ))}
    )
    def get(self, request, quarter):
        from datetime import timedelta

        if quarter not in [1, 2, 3, 4]:
            return Response(
                {'error': 'Квартал должен быть от 1 до 4'},
                status=status.HTTP_400_BAD_REQUEST
            )

        year = 2026
        start_month = (quarter - 1) * 3 + 1
        start_date = date(year, start_month, 1)

        if quarter == 4:
            end_date = date(year, 12, 31)
        else:
            end_date = date(year, start_month + 3, 1) - timedelta(days=1)

        clients_per_room = Stay.objects.filter(
            check_in__range=[start_date, end_date]
        ).values('room__number').annotate(
            client_count=Count('client', distinct=True)
        )

        rooms_per_floor = Room.objects.values('floor').annotate(
            room_count=Count('id')
        )

        stays = Stay.objects.filter(
            check_in__range=[start_date, end_date]
        ).select_related('room')

        income_per_room = {}
        total_income = 0

        for stay in stays:
            days = (stay.check_out - stay.check_in).days
            income = days * float(stay.room.price_per_day)
            total_income += income

            room_num = stay.room.number
            if room_num not in income_per_room:
                income_per_room[room_num] = 0
            income_per_room[room_num] += income

        return Response({
            'quarter': quarter,
            'year': year,
            'period': f'{start_date} - {end_date}',
            'clients_per_room': list(clients_per_room),
            'rooms_per_floor': list(rooms_per_floor),
            'income_per_room': income_per_room,
            'total_income': total_income
        })
