from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import datetime, date
from rest_framework import status
from django.db.models import Count, Sum
from .permissions import IsAdminUser
from .models import Room, Client, Staff, CleaningSchedule, Reservation, Report
from .serializers import (
    RoomSerializer,
    ClientSerializer,
    StaffSerializer,
    CleaningScheduleSerializer,
    ReservationSerializer,
    ReportSerializer,
)


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='available-rooms')
    def available_rooms(self, request, *args, **kwargs):
        today = date.today()

        available_rooms_count = Room.objects.filter(
            is_occupied=False
        ).exclude(
            reservations__check_in_date__lte=today,
            reservations__check_out_date__gte=today
        ).count()

        return Response({'available_rooms': available_rooms_count}, status=status.HTTP_200_OK)


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(detail=False, methods=['get'],
            url_path='by-room-period/(?P<room_id>\d+)/(?P<start_date>[\d\-]+)/(?P<end_date>[\d\-]+)')
    def clients_by_room_period(self, request, room_id, start_date, end_date, *args, **kwargs):
        clients = Client.objects.filter(
            reservations__room__id=room_id,
            reservations__check_in_date__lte=end_date,
            reservations__check_out_date__gte=start_date
        ).distinct()
        serializer = self.get_serializer(clients, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-city/(?P<city>[\w\s]+)')
    def clients_by_city(self, request, city, *args, **kwargs):
        client_count = Client.objects.filter(city=city).count()
        return Response({'client_count': client_count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'],
            url_path='shared-stay/(?P<client_id>\d+)/(?P<start_date>[\d\-]+)/(?P<end_date>[\d\-]+)')
    def shared_stay(self, request, client_id, start_date, end_date, *args, **kwargs):
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        client_reservations = Reservation.objects.filter(client_id=client_id)

        overlapping_reservations = Reservation.objects.filter(
            check_in_date__lte=end_date,
            check_out_date__gte=start_date
        ).exclude(client_id=client_id)

        shared_clients = Client.objects.filter(
            reservations__in=overlapping_reservations
        ).distinct()

        serializer = self.get_serializer(shared_clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StaffViewSet(ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='cleaning-by-client-day(?:/(?P<client_id>\d+))?(?:/(?P<weekday>\w+))?')
    def cleaning_by_client_day(self, request, client_id=None, weekday=None, *args, **kwargs):
        if client_id and weekday:
            staff_members = Staff.objects.filter(
                schedules__client__id=client_id,
                schedules__day_of_week__iexact=weekday
            ).distinct()
        elif client_id:
            staff_members = Staff.objects.filter(
                schedules__client__id=client_id
            ).distinct()
        else:
            staff_members = Staff.objects.all()

        serializer = self.get_serializer(staff_members, many=True)
        return Response(serializer.data)

class CleaningScheduleViewSet(ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    @action(detail=False, methods=['get'], url_path='generate-report/(?P<quarter>\d+)')
    def generate_report(self, request, quarter, *args, **kwargs):
        try:
            quarter = int(quarter)
        except ValueError:
            return Response({'error': 'Quarter must be between 1 and 4'}, status=400)

        if quarter not in [1, 2, 3, 4]:
            return Response({'error': 'Quarter must be between 1 and 4'}, status=400)

        year = datetime.now().year

        if quarter == 1:
            start_date = f"{year}-01-01"
            end_date = f"{year}-03-31"
        elif quarter == 2:
            start_date = f"{year}-04-01"
            end_date = f"{year}-06-30"
        elif quarter == 3:
            start_date = f"{year}-07-01"
            end_date = f"{year}-09-30"
        elif quarter == 4:
            start_date = f"{year}-10-01"
            end_date = f"{year}-12-31"

        rooms = Room.objects.annotate(
            total_clients=Count('reservations', filter=Q(
                reservations__check_in_date__lte=end_date,
                reservations__check_out_date__gte=start_date
            )),
            total_income=Sum('reservations__room__price_per_day', filter=Q(
                reservations__check_in_date__lte=end_date,
                reservations__check_out_date__gte=start_date
            ))
        ).values('id', 'number', 'total_clients', 'total_income') or []

        floors = Room.objects.values('floor').annotate(num_rooms=Count('id')) or []

        total_income = Reservation.objects.filter(
            check_in_date__gte=start_date, check_out_date__lte=end_date
        ).aggregate(total_income=Sum('room__price_per_day'))['total_income']

        if total_income is None:
            total_income = 0

        report_data = {
            'year': year,
            'quarter': quarter,
            'rooms': list(rooms),
            'floors': list(floors),
            'total_income': total_income
        }

        return Response(report_data, status=status.HTTP_200_OK)