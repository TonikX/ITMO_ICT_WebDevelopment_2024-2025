from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from accounts.models import UserProfile
from booking.models import Booking
from rooms.models import Floor
from staff.models import Employee, RoomClean
from staff.serializers import EmployeeSerializer, RoomCleanSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class RoomCleanViewSet(viewsets.ModelViewSet):
    queryset = RoomClean.objects.all()
    serializer_class = RoomCleanSerializer

@api_view(["GET"])
@csrf_exempt
def get_cleaner_rooms(request):
    last_name = request.query_params.get('name')
    date = request.query_params.get('date')
    user = UserProfile.objects.get(last_name=last_name).id
    room_id = Booking.objects.filter(guest_id=user)[0].room_id.floor.id
    cleaner = RoomClean.objects.get(floor=room_id, clean_date=date).worker_id
    return JsonResponse({'name': cleaner.full_name, "rank": cleaner.rank}, safe=False, status=status.HTTP_200_OK)
