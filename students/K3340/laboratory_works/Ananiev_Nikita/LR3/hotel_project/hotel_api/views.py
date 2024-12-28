from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from .serializers import *


class RoomAPIView(generics.RetrieveAPIView):
    serializer_class = RoomDetailedSerializer
    lookup_field = 'id'
    queryset = Room.objects.all()


class RoomListAPIView(generics.ListAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


class RoomUpdateAPIView(generics.UpdateAPIView):
    serializer_class = RoomUpdateSerializer
    lookup_field = 'id'
    queryset = Room.objects.all()


class RoomTypeListAPIView(generics.ListAPIView):
    serializer_class = RoomTypeSerializer
    queryset = RoomType.objects.all()
