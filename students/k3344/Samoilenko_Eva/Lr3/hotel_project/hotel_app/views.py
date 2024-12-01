from datetime import datetime, timedelta
from django.db.models import Q
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


class RoomsAPIView(APIView):
    serializer_class = RoomSerializer

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response({'List of Hotel Rooms': serializer.data})

    @swagger_auto_schema(request_body=RoomCreateSerializer)
    def post(self, request):
        post_serializer = self.serializer_class(data=request.data)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        return Response({'Created new Room': post_serializer.data}, status=status.HTTP_201_CREATED)


class RoomAPIView(APIView):
    def get(self, request, room_id=None):
        try:
            room = Room.objects.get(id=room_id)
            serializer = RoomSerializer(room)
            return Response({f'{room.__str__()}': serializer.data})
        except Room.DoesNotExist:
            return Response({"Not Found": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, room_id=None):
        try:
            room = Room.objects.get(id=room_id)
            room.delete()
            return Response({f'Deleted {room.__str__()}'}, status=status.HTTP_204_NO_CONTENT)
        except Room.DoesNotExist:
            return Response({"Not Found": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=RoomCreateSerializer)
    def patch(self, request, room_id=None):
        try:
            room = Room.objects.get(id=room_id)
            serializer = RoomCreateSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({f'Updated {room.__str__()}': serializer.data},
                                status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({"Not Found": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeesAPIView(APIView):
    serializer_class = EmployeeSerializer

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response({'List of all hired Employees': serializer.data})

    @swagger_auto_schema(request_body=EmployeeCreateSerializer)
    def post(self, request):
        post_serializer = EmployeeCreateSerializer(data=request.data)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        return Response({'Created new Employee': post_serializer.data},
                        status=status.HTTP_201_CREATED)


class EmployeeAPIView(APIView):
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
            serializer = EmployeeSerializer(employee)
            return Response({f'{employee.__str__()}': serializer.data})
        except Employee.DoesNotExist:
            return Response({"Not Found": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
            employee.delete()
            return Response({f'Deleted {employee.__str__()}'}, status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({"Not Found": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=EmployeeCreateSerializer)
    def patch(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({"Not Found": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeCreateSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({f'Updated {employee.__str__()}': serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientsAPIView(APIView):
    serializer_class = ClientSerializer

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response({'List of all existing Clients': serializer.data})

    @swagger_auto_schema(request_body=ClientCreateSerializer)
    def post(self, request):
        post_serializer = ClientCreateSerializer(data=request.data)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        return Response({'Created new Client': post_serializer.data},
                        status=status.HTTP_201_CREATED)


class ClientAPIView(APIView):
    def get(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
            serializer = ClientSerializer(client)
            return Response({f'{client.__str__()}': serializer.data})
        except Client.DoesNotExist:
            return Response({"Not Found": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
            client.delete()
            return Response({f'Deleted {client.__str__()}'}, status=status.HTTP_204_NO_CONTENT)
        except Client.DoesNotExist:
            return Response({"Not Found": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=ClientCreateSerializer)
    def patch(self, request, client_id):
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({"Not Found": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClientCreateSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({f'Updated {client.__str__()}': serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingsAPIView(APIView):
    serializer_class = BookingSerializer

    def get(self, request):
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response({'List of all Bookings': serializer.data})

    @swagger_auto_schema(request_body=BookingCreateSerializer)
    def post(self, request):
        post_serializer = self.serializer_class(data=request.data)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        return Response({'Created new Booking': post_serializer.data},
                        status=status.HTTP_201_CREATED)


class BookingAPIView(APIView):
    def get(self, request, booking_id=None):
        try:
            booking = Booking.objects.get(id=booking_id)
            serializer = BookingSerializer(booking)
            return Response({f'{booking.__str__()}': serializer.data})
        except Booking.DoesNotExist:
            return Response({"Not Found": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, booking_id=None):
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.delete()
            return Response({f'Deleted {booking.__str__()}'}, status=status.HTTP_204_NO_CONTENT)
        except Booking.DoesNotExist:
            return Response({"Not Found": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=BookingCreateSerializer)
    def patch(self, request, booking_id=None):
        try:
            booking = Booking.objects.get(id=booking_id)
            serializer = BookingCreateSerializer(booking, data=request.data, partial=True)
        except Booking.DoesNotExist:
            return Response({"Not Found": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response({f'Updated {booking.__str__()}': serializer.data},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CleaningsAPIView(APIView):
    serializer_class = CleaningSerializer

    def get(self, request):
        cleanings = Cleaning.objects.all()
        serializer = CleaningSerializer(cleanings, many=True)
        return Response({'List of all Cleanings': serializer.data})

    @swagger_auto_schema(request_body=CleaningCreateSerializer)
    def post(self, request):
        post_serializer = self.serializer_class(data=request.data)
        post_serializer.is_valid(raise_exception=True)
        post_serializer.save()
        return Response({'Created new Cleaning': post_serializer.data},
                        status=status.HTTP_201_CREATED)


class CleaningAPIView(APIView):
    def get(self, request, cleaning_id=None):
        try:
            cleaning = Cleaning.objects.get(id=cleaning_id)
            serializer = CleaningSerializer(cleaning)
            return Response({f'{cleaning.__str__()}': serializer.data})
        except Cleaning.DoesNotExist:
            return Response({"Not Found": "Cleaning not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, cleaning_id=None):
        try:
            cleaning = Cleaning.objects.get(id=cleaning_id)
            cleaning.delete()
            return Response({f'Deleted {cleaning.__str__()}'}, status=status.HTTP_204_NO_CONTENT)
        except Cleaning.DoesNotExist:
            return Response({"Not Found": "Cleaning not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=CleaningCreateSerializer)
    def patch(self, request, cleaning_id=None):
        try:
            cleaning = Cleaning.objects.get(id=cleaning_id)
            serializer = CleaningCreateSerializer(cleaning, data=request.data, partial=True)
        except Cleaning.DoesNotExist:
            return Response({"Not Found": "Cleaning not found"}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save()
            return Response({f'Updated {cleaning.__str__()}': serializer.data},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientsInRoomView(APIView):
    """Клиенты, проживавшие в заданном номере в заданный период времени
    (e. g. room_id=6, start_date=2024-09-21, end_date=2024-11-01)
    """
    def get(self, request, room_id, start_date, end_date):
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

        bookings = Booking.objects.filter(
            room_id=room_id,
            end_date__lte=end_date,
            start_date__gte=start_date
        ).select_related('client')

        clients = [booking.client for booking in bookings]

        serializer = ClientSerializer(clients, many=True)
        if len(serializer.data) == 0:
            return Response({f'There were no Clients in Room {room_id} in a date range (from'
                             f' {start_date} to '
                             f'{end_date})'},
                            status=status.HTTP_200_OK)

        return Response({f'Clients in Room {room_id} in a date range (from {start_date} to '
                         f'{end_date})': serializer.data},
                        status=status.HTTP_200_OK)


class ClientsFromCityView(APIView):
    """Количество клиентов, прибывших из заданного города
    (e. g. Forks or London)
    """
    def get(self, request, origin_city):
        origin_city = origin_city.capitalize()
        client_count = Client.objects.filter(origin_city=origin_city).count()

        data = {
            "origin_city": origin_city,
            "client_count": client_count
        }
        return Response({f'Amount of Clients from {origin_city}': data}, status=status.HTTP_200_OK)


class EmployeesWhoCleanedView(APIView):
    """
    Кто из служащих убирал номер указанного клиента в заданный день недели
    (e. g. client_id=1 and week_day=Fri)
    """
    def get(self, request, client_id, week_day):
        try:
            booking = Booking.objects.get(client_id=client_id)
        except Booking.DoesNotExist:
            return Response({"Not Found": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        floor_num = booking.room.floor_num
        cleanings = Cleaning.objects.filter(floor_num=floor_num,
                                            week_day=week_day).select_related('employee')

        employees = set([cleaning.employee for cleaning in cleanings])

        serializer = EmployeeSerializer(employees, many=True)
        if len(serializer.data) == 0:
            return Response({f'No Employees cleaned {booking.client.__str__()}\'s Room on'
                             f' {week_day}'}, status=status.HTTP_200_OK)

        return Response({f'Employee/s, who cleaned {booking.client.__str__()}\'s Room on'
                         f' {week_day}':
                        serializer.data},
                        status=status.HTTP_200_OK)


# Сколько в гостинице свободных номеров
class FreeRoomsView(APIView):
    """
        Сколько в гостинице свободных номеров в заданный промежуток времени
        (e. g. 2024-10-30/2024-11-30)
    """
    def get(self, request, start_date, end_date):
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

        busy_room_count = Booking.objects.filter(start_date__gte=start_date,
                                                 end_date__lte=end_date).count()
        free_rooms = Hotel.objects.all()[0].num_rooms - busy_room_count

        data = {
            "start_date": start_date,
            "end_date": end_date,
            "free_rooms_count": free_rooms
        }

        return Response({'Amount of free Rooms in specific daterange': data})


class ClientsWhileClientView(APIView):
    """
        Список клиентов с указанием места жительства, которые проживали в отеле в те же дни,
        что и заданный клиент
    """
    def get(self, request, request_client_id):
        bookings = Booking.objects.filter(client_id=request_client_id)

        if not bookings.exists():
            return Response({"error": "Specified client has no bookings."},
                            status=status.HTTP_404_NOT_FOUND)

        specified_client_dates = []
        for booking in bookings:
            specified_client_dates.append((booking.start_date, booking.end_date))

        query = Q()
        for start, end in specified_client_dates:
            query |= Q(start_date__lt=end, end_date__gt=start)

        overlapping_bookings = Booking.objects.filter(query).exclude(client_id=request_client_id)
        overlapping_clients = Client.objects.filter(
            booking_client__in=overlapping_bookings).distinct()

        serializer = ClientSerializer(overlapping_clients, many=True)
        return Response({f'When your requested client stayed in our hotel, these clients were '
                         f'also here': serializer.data},
                        status=status.HTTP_200_OK)
