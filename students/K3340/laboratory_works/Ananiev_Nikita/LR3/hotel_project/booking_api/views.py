from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import generics

from .serializers import *


class BookingAPIView(generics.RetrieveAPIView):
    serializer_class = BookingDetailedSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    queryset = Booking.objects.all()


class BookingListAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Booking.objects.all()


class BookingCreateAPIView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Booking.objects.all()


class BookingUpdateAPIView(generics.UpdateAPIView):
    serializer_class = BookingUpdateSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'id'
    queryset = Booking.objects.all()


class BookingDeleteAPIView(generics.DestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'id'
    queryset = Booking.objects.all()