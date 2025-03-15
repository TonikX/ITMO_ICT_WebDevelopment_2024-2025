from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializers import (
    Contract,
    ContractCreateSerializer,
    ContractDetailedSerializer,
    ContractSerializer,
    ContractUpdateSerializer,
    Employee,
    EmployeeSerializer,
    Position,
    PositionSerializer,
    ScheduleCreateSerializer,
    ScheduleDetailedSerializer,
    ScheduleSerializer,
    ScheduleUpdateSerializer,
    WorkSchedule,
)


class EmployeeAPIView(RetrieveAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    queryset = Employee.objects.all()


class EmployeeListAPIView(ListAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()


class EmployeeCreateAPIView(CreateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = (IsAdminUser,)
    queryset = Employee.objects.all()


class PositionAPIView(RetrieveAPIView):
    serializer_class = PositionSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    queryset = Position.objects.all()


class PositionListAPIView(ListAPIView):
    serializer_class = PositionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Position.objects.all()


class ContractAPIView(RetrieveAPIView):
    serializer_class = ContractDetailedSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    queryset = Contract.objects.all()


class ContractListAPIView(ListAPIView):
    serializer_class = ContractSerializer
    permission_classes = (IsAdminUser,)
    queryset = Contract.objects.all()


class ContractCreateAPIView(CreateAPIView):
    serializer_class = ContractCreateSerializer
    permission_classes = (IsAdminUser,)
    queryset = Contract.objects.all()


class ContractUpdateAPIView(UpdateAPIView):
    serializer_class = ContractUpdateSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'id'
    queryset = Contract.objects.all()


class ContractDeleteAPIView(DestroyAPIView):
    serializer_class = ContractSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'id'
    queryset = Contract.objects.all()


class ScheduleAPIView(RetrieveAPIView):
    serializer_class = ScheduleDetailedSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    queryset = WorkSchedule.objects.all()


class ScheduleListAPIView(ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = (IsAuthenticated,)
    queryset = WorkSchedule.objects.all()


class ScheduleCreateAPIView(CreateAPIView):
    serializer_class = ScheduleCreateSerializer
    permission_classes = (IsAdminUser,)
    queryset = WorkSchedule.objects.all()


class ScheduleUpdateAPIView(UpdateAPIView):
    serializer_class = ScheduleUpdateSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'id'
    queryset = WorkSchedule.objects.all()


class ScheduleDeleteAPIView(DestroyAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'id'
    queryset = WorkSchedule.objects.all()
