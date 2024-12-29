from rest_framework import viewsets
from .models import Floor, Room, Client, StayRecord, Employee, CleaningSchedule, CleaningRecord
from .serializers import (
    FloorSerializer, RoomSerializer, ClientSerializer,
    StayRecordSerializer, EmployeeSerializer,
    CleaningScheduleSerializer, CleaningRecordSerializer
)


class FloorViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class StayRecordViewSet(viewsets.ModelViewSet):
    queryset = StayRecord.objects.all()
    serializer_class = StayRecordSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer


class CleaningRecordViewSet(viewsets.ModelViewSet):
    queryset = CleaningRecord.objects.all()
    serializer_class = CleaningRecordSerializer
