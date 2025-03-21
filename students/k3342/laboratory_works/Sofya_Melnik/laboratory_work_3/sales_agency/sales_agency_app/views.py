from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from django.utils.timezone import now
from django.utils.dateparse import parse_date
from datetime import timedelta
from rest_framework.exceptions import ValidationError as DRFValidationError

from .models import Client, Service, PriceList, Position, Employee, PositionEmployee, Order, PaymentOrder
from .serializers import (
    ClientSerializer, ServiceSerializer, PriceListSerializer, PositionSerializer,
    EmployeeSerializer, PositionEmployeeSerializer, OrderSerializer, PaymentOrderSerializer
)
from .permissions import IsClient, IsAdmin


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsClient]

class PriceListViewSet(viewsets.ModelViewSet):
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    permission_classes = [IsAuthenticated, IsClient]

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class PositionEmployeeViewSet(viewsets.ModelViewSet):
    queryset = PositionEmployee.objects.all()
    serializer_class = PositionEmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsClient]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user.client)

    def get_queryset(self):
        if self.request.user.is_staff:
            # Администратор видит все заказы
            return Order.objects.all()
        # Клиент видит только свои заказы
        return Order.objects.filter(client=self.request.user.client)


class PaymentOrderViewSet(viewsets.ModelViewSet):
    queryset = PaymentOrder.objects.all()
    serializer_class = PaymentOrderSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsClient]

    def get_queryset(self):
        if self.request.user.is_staff:
            # Администратор видит все платежи
            return PaymentOrder.objects.all()
        # Клиент видит только свои платежи
        return PaymentOrder.objects.filter(client=self.request.user.client)


# 1. Список выполненных работ
class CompletedOrdersListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return Order.objects.filter(status='completed')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().values(
            'completion_date', 'client__first_name', 'client__last_name', 'service__id', 'employee__last_name'
        )
        return Response(list(queryset))


# 2. Список платежных поручений за период
class PaymentOrdersByPeriodView(generics.ListAPIView):
    serializer_class = PaymentOrderSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        try:
            start_date = parse_date(start_date) if start_date else None
            end_date = parse_date(end_date) if end_date else None
        except:
            raise DRFValidationError({"error": "Неверный формат даты. Используйте YYYY-MM-DD."})

        if start_date and end_date:
            return PaymentOrder.objects.filter(payment_order_date__range=[start_date, end_date])
        return PaymentOrder.objects.all()


# 3. Просмотр номенклатуры рекламных услуг
class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsClient]


# 4. Список заявок заказчика за период
class OrdersByClientView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsClient]

    def get_queryset(self):
        return Order.objects.none()


# 5. Список сотрудников с количеством выполненных заявок
class EmployeeOrdersCountView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            return Employee.objects.annotate(
                order_count=Count('order', distinct=True)
            ).filter(order__order_date__range=[start_date, end_date])
        return Employee.objects.none()


# 6. Отчет о стоимости работ за последний квартал
class QuarterlyReportView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, *args, **kwargs):
        last_quarter = now() - timedelta(days=90)
        report = Order.objects.filter(completion_date__gte=last_quarter).aggregate(total_cost=Sum('total_cost'))
        return Response(report)
