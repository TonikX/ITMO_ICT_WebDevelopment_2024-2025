from rest_framework import viewsets, filters
from rest_framework import status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Sum, F, Q
from rest_framework.views import APIView
from datetime import date, datetime

from .models import Room, Client, Staff, Stay, CleaningSchedule, CleaningExecution
from .serializers import (
    RoomSerializer, ClientSerializer, StaffSerializer, StaySerializer,
    CleaningScheduleSerializer, CleaningExecutionSerializer
)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['room_type', 'floor']
    search_fields = ['phone_number', 'room_id']

    @action(detail=False, methods=['get'])
    def available_rooms_count(self, request):
        count = Room.objects.filter(is_available=True).count()
        return Response({'available_rooms': count})


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    # permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city_of_origin']
    search_fields = ['last_name', 'first_name', 'passport_number']

    @action(detail=False, methods=['get'])
    def count_by_city(self, request):
        city = request.query_params.get('city')
        if not city:
            return Response({'error': 'Необходимо указать параметр city'}, status=400)
        
        count = Client.objects.filter(city_of_origin=city).count()
        return Response({'city': city, 'client_count': count})
    
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """
        Возвращает объект Client, связанный с текущим пользователем.
        Предполагается, что в модели Client есть поле user = OneToOneField(User).
        """
        if not request.user.is_authenticated:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Пытаемся найти Client, связанного с request.user
        try:
            client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            return Response({'detail': 'Данные клиента не найдены'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def clients_shared_stay(self, request):
        client_id = request.query_params.get('client_id')
        if not client_id:
            return Response({'error': 'Необходимо указать client_id'}, status=400)

        try:
            client = Client.objects.get(client_id=client_id)
        except Client.DoesNotExist:
            return Response({'error': 'Клиент не найден'}, status=404)

        client_stays = Stay.objects.filter(client=client)

        overlapping_conditions = Q()
        for stay in client_stays:
            overlapping_conditions |= (
                Q(check_in_date__lte=stay.check_out_date) & Q(check_out_date__gte=stay.check_in_date)
            )

        overlapping_stays = Stay.objects.filter(
            overlapping_conditions,
            ~Q(client=client)
        ).select_related('client')

        other_clients = {stay.client for stay in overlapping_stays}

        serializer = ClientSerializer(other_clients, many=True)
        return Response(serializer.data)

    # permission_classes = [IsAuthenticated]
    #
    # def get_queryset(self):
    #     user = self.request.user
    #     return Client.objects.filter(user=user)
    #
    # def perform_create(self, serializer):
    #     serializer.save()

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['last_name', 'first_name']

class StayViewSet(viewsets.ModelViewSet):
    queryset = Stay.objects.all()
    serializer_class = StaySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['client__client_id', 'room__room_id', 'check_in_date', 'check_out_date']
    search_fields = ['client__last_name', 'room__room_id']

    @action(detail=False, methods=['get'])
    def stays_in_room(self, request):
        room_id = request.query_params.get('room_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not room_id or not start_date or not end_date:
            return Response({'error': 'Необходимо указать room_id, start_date и end_date'}, status=400)

        stays = Stay.objects.filter(
            room__room_id=room_id,
            check_in_date__lte=end_date,
            check_out_date__gte=start_date
        )

        serializer = self.get_serializer(stays, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        stay = serializer.save()
        stay.room.is_available = False
        stay.room.save()

    def perform_update(self, serializer):
        stay = serializer.save()
        if stay.check_out_date and stay.check_out_date <= date.today():
            stay.room.is_available = True
        else:
            stay.room.is_available = False
        stay.room.save()

    def perform_destroy(self, instance):
        room = instance.room
        instance.delete()
        room.is_available = True
        room.save()
    
    @action(detail=False, methods=['get'], url_path='user')
    def user(self, request):
        """
        Возвращает список всех Stay (проживаний) текущего пользователя.
        """
        if not request.user.is_authenticated:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Ищем Client, связанный с пользователем:
        try:
            client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            # Если у пользователя нет Client, вернём пустой список
            return Response([], status=status.HTTP_200_OK)
        
        # Выбираем все Stay, связанные с этим client:
        user_stays = Stay.objects.filter(client=client).select_related('room')
        serializer = self.get_serializer(user_stays, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['staff__staff_id', 'floor', 'time_and_day_of_week']
    search_fields = ['staff__last_name', 'time_and_day_of_week']

class CleaningExecutionViewSet(viewsets.ModelViewSet):
    queryset = CleaningExecution.objects.all()
    serializer_class = CleaningExecutionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['staff__staff_id', 'floor', 'time_and_day_of_week']
    search_fields = ['staff__last_name', 'time_and_day_of_week']

    @action(detail=False, methods=['get'])
    def staff_cleaned_client_room(self, request):
        client_id = request.query_params.get('client_id')
        day_of_week = request.query_params.get('day_of_week')

        if not client_id or not day_of_week:
            return Response({'error': 'Необходимо указать client_id и day_of_week'}, status=400)

        # Находим последние пребывание клиента
        stay = Stay.objects.filter(client__client_id=client_id).last()
        if not stay:
            return Response({'error': 'Пребывание клиента не найдено'}, status=404)

        # Фильтруем уборки по номеру и дню недели
        cleanings = CleaningExecution.objects.filter(
            room=stay.room,
            time_and_day_of_week__icontains=day_of_week
        ).select_related('staff')

        staff_members = [cleaning.staff for cleaning in cleanings]
        serializer = StaffSerializer(staff_members, many=True)
        return Response(serializer.data)
    
class ReportView(APIView):

    def get(self, request):
        quarter = request.query_params.get('quarter')
        if not quarter:
            return Response({'error': 'Необходимо указать параметр quarter (1-4)'}, status=400)

        try:
            quarter = int(quarter)
            if quarter not in [1, 2, 3, 4]:
                raise ValueError
        except ValueError:
            return Response({'error': 'Параметр quarter должен быть числом от 1 до 4'}, status=400)

        # Определяем начало и конец квартала
        year = datetime.now().year
        if quarter == 1:
            start_date = datetime(year, 1, 1).date()
            end_date = datetime(year, 3, 31).date()
        elif quarter == 2:
            start_date = datetime(year, 4, 1).date()
            end_date = datetime(year, 6, 30).date()
        elif quarter == 3:
            start_date = datetime(year, 7, 1).date()
            end_date = datetime(year, 9, 30).date()
        else:
            start_date = datetime(year, 10, 1).date()
            end_date = datetime(year, 12, 31).date()

        # 1. Число клиентов за указанный период в каждом номере
        stays_per_room = Stay.objects.filter(
            check_in_date__lte=end_date,
            check_out_date__gte=start_date
        ).values('room__room_id').annotate(client_count=Count('client', distinct=True))

        # 2. Количество номеров на каждом этаже
        rooms_per_floor = Room.objects.values('floor').annotate(room_count=Count('room_id'))

        # 3. Общая сумма дохода за каждый номер
        stays = Stay.objects.filter(
            check_in_date__lte=end_date,
            check_out_date__gte=start_date
        )
        income_per_room = {}
        total_income = 0
        for stay in stays:
            actual_check_in = max(stay.check_in_date, start_date)
            actual_check_out = min(stay.check_out_date, end_date)
            duration = (actual_check_out - actual_check_in).days
            income = duration * float(stay.room.cost_per_day)
            income_per_room[stay.room.room_id] = income_per_room.get(stay.room.room_id, 0) + income
            total_income += income

        # Преобразуем доход по номерам в ожидаемый формат
        income_per_room = [{'room_id': room_id, 'total_income': income} for room_id, income in income_per_room.items()]

        report = {
            'stays_per_room': list(stays_per_room),
            'rooms_per_floor': list(rooms_per_floor),
            'income_per_room': income_per_room,
            'total_income': total_income
        }

        return Response(report)