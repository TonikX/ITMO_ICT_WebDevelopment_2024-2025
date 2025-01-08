from django.db.models import DateField
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from booking.models import Booking
from booking.serializers import BookingSerializer, BookingRoomSerializer
from rooms.models import RoomType, Room, Floor
from rooms.serializers import RoomTypeSerializer, FloorSerializer, RoomSerializer


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAuthenticated]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class FloorViewSet(viewsets.ModelViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer



@api_view(["GET"])
@csrf_exempt
def get_rooms(request):
    room = request.query_params.get('room_id')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    rooms = Booking.objects.filter(room_id=room).filter(book_date__range=(start_date, end_date))
    serializer = BookingRoomSerializer(rooms, many=True)
    return JsonResponse({'rooms': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
def get_empty_rooms(request):

    rooms = Room.objects.filter(is_occupied=True)
    serializer = RoomSerializer(rooms, many=True)
    return JsonResponse({'rooms': len(serializer.data)}, safe=False, status=status.HTTP_200_OK)
