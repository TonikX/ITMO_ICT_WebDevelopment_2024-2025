from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import IsAuthenticated

from booking.models import Booking
from booking.serializers import BookingSerializer
from .models import UserProfile
from .permission import IsOwnerProfileOrReadOnly
from .serializers import UserProfileSerializer

# Create your views here.

class UserProfileListCreateView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerProfileOrReadOnly,IsAuthenticated]

@api_view(["GET"])
@csrf_exempt
def get_guests(request):
    city = request.query_params.get('city')
    guests = UserProfile.objects.filter(city=city)
    serializer = UserProfileSerializer(guests, many=True)
    return JsonResponse({'count': len(serializer.data)}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
def get_guests_on_neighbour(request):
    name = request.query_params.get('name')
    guests = UserProfile.objects.get(last_name=name)
    dates = Booking.objects.get(guest_id=guests).book_date
    other_books = Booking.objects.filter(book_date=dates)
    data = {'guests': []}
    for book in other_books:
        data['guests'].append([book.guest_id.last_name, book.guest_id.city])


    return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
