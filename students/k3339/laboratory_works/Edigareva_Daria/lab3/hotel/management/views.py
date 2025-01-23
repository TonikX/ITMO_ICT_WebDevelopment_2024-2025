from rest_framework import generics
from .models import Room, Client, Booking, Staff, CleaningSchedule, CleaningConfirmation
from .serializers import RoomSerializer, ClientSerializer, BookingSerializer, StaffSerializer, CleaningScheduleSerializer, CleaningConfirmationSerializer

class RoomListCreateAPIView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ClientListCreateAPIView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


# Bookings
class BookingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class BookingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class StaffListCreateAPIView(generics.ListCreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StaffDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


# Cleaning Schedules
class CleaningScheduleListCreateAPIView(generics.ListCreateAPIView):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer


class CleaningScheduleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CleaningSchedule.objects.all()
    serializer_class = CleaningScheduleSerializer


class CleaningConfirmationListCreateAPIView(generics.ListCreateAPIView):
    queryset = CleaningConfirmation.objects.all()
    serializer_class = CleaningConfirmationSerializer


class CleaningConfirmationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CleaningConfirmation.objects.all()
    serializer_class = CleaningConfirmationSerializer
