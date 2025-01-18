from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAdminUser, IsAuthenticated
from . import serializers
from .models import *


class AnimalViewSet(ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = serializers.AnimalSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    @action(detail=False, methods=["GET"])
    def animals_in_lease(self,request ):
        qs = Animal.objects.filter(in_lease=True)
        ser = self.serializer_class(qs, many=True)
        return ser.data

    @action(detail=False, methods=['get'])
    def animals_in_lease(self, request):
        qs = self.get_queryset().filter(in_lease=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["GET"])
    def leaving_together(self, request, pk=None):
        animal = self.get_object()
        qs = self.queryset.filter(where=animal.where)
        ser = self.serializer_class(qs, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def animals_in(self, request):
        ser = serializers.CountAnimalInArea(Area.objects.all(), many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def show_empty(self, request):
        qs = Cage.objects.none()
        for obj in Cage.objects.all():
            if AnimalInCage.objects.filter(cage=obj.id).count() == 0:
                qs |= Cage.objects.filter(id=obj.id)

        ser = serializers.CageSerializer(qs, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)


class AreaViewSet(ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = serializers.AreaSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class CageViewSet(ModelViewSet):
    queryset = Cage.objects.all()
    serializer_class = serializers.CageSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class DietViewSet(ModelViewSet):
    queryset = Diet.objects.all()
    serializer_class = serializers.DietSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class HabitatViewSet(ModelViewSet):
    queryset = Habitat.objects.all()
    serializer_class = serializers.HabitatSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class WinterPlaceViewSet(ModelViewSet):
    queryset = WinterPlace.objects.all()
    serializer_class = serializers.WinterPlaceSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class AnimalInCageViewSet(ModelViewSet):
    queryset = AnimalInCage.objects.all()
    serializer_class = serializers.AnimalInCageSerializer

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]
