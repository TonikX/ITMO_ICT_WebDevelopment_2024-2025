from rest_framework import viewsets, permissions
from .models import Client, RoomType, Room, RoomPrice, Booking, JobTitle, Employee, EmploymentContract, CleaningSchedule
from .serializers import (
    ClientSerializer,
    RoomTypeSerializer,
    RoomSerializer,
    RoomPriceSerializer,
    BookingSerializer,
    JobTitleSerializer,
    EmployeeSerializer,
    EmploymentContractSerializer,
    CleaningScheduleSerializer
)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RoomPriceViewSet(viewsets.ModelViewSet):
    queryset = RoomPrice.objects.all()
    serializer_class = RoomPriceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class JobTitleViewSet(viewsets.ModelViewSet):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EmploymentContractViewSet(viewsets.ModelViewSet):
    queryset = EmploymentContract.objects.all()
    serializer_class = EmploymentContractSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CleaningScheduleViewSet(viewsets.ModelViewSet):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]