from datetime import datetime

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .permissions import IsOwnerOrReadonly
from .serializers import *
from .utils import parse_or_return, check_if_can_book


# Create your views here.
class RestaurantListCreateView(ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RestaurantDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all().prefetch_related('table_set')
    serializer_class = RestaurantDetailSerializer
    permission_classes = [IsOwnerOrReadonly]


class TableListView(ListAPIView):
    serializer_class = TableWithReservationSerializer

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])

        date = self.request.GET.get('date') or datetime.today().date()

        reservations = Reservation.objects.filter(
            table__restaurant=restaurant,
            dt_reservation=parse_or_return(date)
        )

        return Table.objects \
            .filter(restaurant=restaurant) \
            .prefetch_related(
            Prefetch('reservation_set',
                     queryset=reservations)
        )


class ReservationCreateView(CreateAPIView):
    serializer_class = ReservationCreateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()

    def perform_create(self, serializer):
        t_start, t_end = serializer.validated_data.get('time_start'), serializer.validated_data.get('time_end')
        date = serializer.validated_data.get('dt_reservation')

        table = get_object_or_404(Table, pk=self.kwargs['tpk'])

        if not check_if_can_book(table, date, t_start, t_end):
            raise ValidationError({'time': "this time is already reserved"})

        serializer.save(user=self.request.user, table=table)


class RestaurantReviewsListCreateView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        return Review.objects.filter(restaurant=restaurant)

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, restaurant=restaurant)


class MyRestaurantsListView(ListAPIView):
    serializer_class = RestaurantListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)


class MyRestaurantBookingListView(ListAPIView):
    serializer_class = ReservationCreateSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        date = self.request.GET.get('date') or datetime.today().date()
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        if restaurant.owner != self.request.user:
            return ValidationError({'time': "Only restaurant owner may know this"})
        return Reservation.objects.filter(
            table__restaurant=restaurant,
            dt_reservation=parse_or_return(date)
        )


class MyRestaurantReviewsListView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        return Review.objects.filter(restaurant=restaurant)


class MyBookingListView(ListAPIView):
    serializer_class = ReservationCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        archive = self.request.GET.get('archive', False)
        if archive:
            return Reservation.objects.filter(user=self.request.user)
        return Reservation.objects.filter(user=self.request.user,
                                          dt_reservation__gt=datetime.today().date())