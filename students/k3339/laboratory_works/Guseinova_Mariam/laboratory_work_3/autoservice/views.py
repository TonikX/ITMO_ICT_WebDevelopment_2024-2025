from rest_framework import viewsets
from django.db.models import Count
from .models import Client, Car, Worker, Service, Order, OrderInfo, PayProcess, Qualification
from .serializers import (
    CustomerSerializer, CarSerializer, EmployeeSerializer,
    ServiceSerializer, OrderSerializer, OrderDetailsSerializer,
    PaymentSerializer, QualificationSerializer
)
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate
from django.db.models import Avg
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from decimal import Decimal

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("Authenticated user:", request.user)
        user = request.user
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,

        }
        return Response(user_data, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Request data:", request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'detail': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        print(f"Username: {username}, Password: {password}")


        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        user_data = [{'id': user.id, 'username': user.username} for user in users]
        return Response(user_data)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = CustomerSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_queryset(self):
        customer_id = self.request.query_params.get('customer_id')
        if customer_id:
            return self.queryset.filter(customer_id=customer_id)
        return self.queryset


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = EmployeeSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        customer_id = request.data.get('customer')
        total_cost = request.data.get('total_cost')

        try:
            customer = Client.objects.get(customer_id=customer_id)
        except Client.DoesNotExist:
            raise ValidationError({"detail": "Customer not found."})


        total_cost_decimal = Decimal(total_cost)
        if customer.balance < total_cost_decimal:
            raise ValidationError({"detail": "Insufficient balance to place the order."})


        customer.balance -= total_cost_decimal
        customer.save(update_fields=['balance'])


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderInfo.objects.all()
    serializer_class = OrderDetailsSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = PayProcess.objects.all()
    serializer_class = PaymentSerializer

class QualificationViewSet(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer


class ServiceAnalytics(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        services_count = OrderInfo.objects.values('service__service_name') \
            .annotate(service_count=Count('order_id')) \
            .order_by('-service_count')

        return Response(services_count)


class OrderStatusAnalytics(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        orders_by_status = Order.objects.values('status') \
            .annotate(status_count=Count('order_id')) \
            .order_by('-status_count')

        return Response(orders_by_status)

class AverageServiceCostView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        average_cost = OrderInfo.objects.aggregate(average_price=Avg('cost'))['average_price']
        return Response({
            "average_service_cost": average_cost
        })

class TopCustomersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        customers = Client.objects.annotate(total_spent=Sum('orders__total_cost')) \
            .order_by('-total_spent')[:10]


        data = [
            {
                "customer_id": customer.customer_id,
                "name": customer.name,
                "total_spent": customer.total_spent
            }
            for customer in customers
        ]

        return Response({"top_customers": data})