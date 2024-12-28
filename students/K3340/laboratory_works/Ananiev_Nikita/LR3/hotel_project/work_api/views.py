from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from .serializers import *


class EmployeeAPIView(RetrieveAPIView):
    serializer_class = EmployeeSerializer
    lookup_field = 'id'
    queryset = Employee.objects.all()


class EmployeeListAPIView(ListAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeeCreateAPIView(CreateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class PositionAPIView(RetrieveAPIView):
    serializer_class = PositionSerializer
    lookup_field = 'id'
    queryset = Position.objects.all()


class PositionListAPIView(ListAPIView):
    serializer_class = PositionSerializer
    queryset = Position.objects.all()


class ContractAPIView(RetrieveAPIView):
    serializer_class = ContractDetailedSerializer
    lookup_field = 'id'
    queryset = Contract.objects.all()


class ContractListAPIView(ListAPIView):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()


class ContractCreateAPIView(CreateAPIView):
    serializer_class = ContractCreateSerializer
    queryset = Contract.objects.all()


class ContractUpdateAPIView(UpdateAPIView):
    serializer_class = ContractUpdateSerializer
    lookup_field = 'id'
    queryset = Contract.objects.all()


class ContractDeleteAPIView(DestroyAPIView):
    serializer_class = ContractSerializer
    lookup_field = 'id'
    queryset = Contract.objects.all()


class ScheduleAPIView(RetrieveAPIView):
    serializer_class = ScheduleDetailedSerializer
    lookup_field = 'id'
    queryset = WorkSchedule.objects.all()


class ScheduleListAPIView(ListAPIView):
    serializer_class = ScheduleSerializer
    queryset = WorkSchedule.objects.all()


class ScheduleCreateAPIView(CreateAPIView):
    serializer_class = ScheduleCreateSerializer
    queryset = WorkSchedule.objects.all()


class ScheduleUpdateAPIView(UpdateAPIView):
    serializer_class = ScheduleUpdateSerializer
    lookup_field = 'id'
    queryset = WorkSchedule.objects.all()


class ScheduleDeleteAPIView(DestroyAPIView):
    serializer_class = ScheduleSerializer
    lookup_field = 'id'
    queryset = WorkSchedule.objects.all()
