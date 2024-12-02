from rest_framework import viewsets
from .models import Customer, Car, Employee, Service, Order, OrderDetails, Payment, Qualification
from .serializers import (
    CustomerSerializer, CarSerializer, EmployeeSerializer,
    ServiceSerializer, OrderSerializer, OrderDetailsSerializer,
    PaymentSerializer, QualificationSerializer
)
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        user_data = [{'id': user.id, 'username': user.username} for user in users]
        return Response(user_data)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class QualificationViewSet(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer
