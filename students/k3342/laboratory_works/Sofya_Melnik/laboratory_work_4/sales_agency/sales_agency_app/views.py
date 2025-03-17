from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import APIView

from django.db.models import Sum, Count, Q
from django.utils.timezone import now
from django.utils.dateparse import parse_date
from datetime import timedelta

from .models import Client, Service, PriceList, Position, Employee, PositionEmployee, Order, PaymentOrder
from .serializers import (
    ClientSerializer, ServiceSerializer, PriceListSerializer, PositionSerializer,
    EmployeeSerializer, PositionEmployeeSerializer, OrderSerializer, PaymentOrderSerializer,
    RegistrationSerializer
)
from .permissions import IsClient, IsAdmin


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Генерируем токены сразу после регистрации
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserClientInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Используем request.user, чтобы получить текущего пользователя
        user = request.user
        
        # Пытаемся найти клиента с таким же email, как у пользователя
        try:
            client = Client.objects.get(email=user.email)
            return Response({
                'id': client.id,
                'first_name': client.first_name,
                'last_name': client.last_name,
                'phone': client.phone,
                'contact_person': client.contact_person,
            })
        except Client.DoesNotExist:
            return Response({"detail": "Client not found."}, status=404)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        
        if user.is_staff:
            serializer.save()
        else:
            raise DRFValidationError({"error": "Создание услуги доступно только администратору."})

    def perform_update(self, serializer):
        user = self.request.user

        if user.is_staff:
            serializer.save()
        else:
            raise DRFValidationError({"error": "Редактирование услуги доступно только администратору."})

    def perform_destroy(self, instance):
        user = self.request.user

        if user.is_staff:
            instance.delete()
        else:
            raise DRFValidationError({"error": "Удаление услуги доступно только администратору."})

class PriceListViewSet(viewsets.ModelViewSet):
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    permission_classes = [IsAuthenticated, IsClient | IsAdmin]

    def perform_create(self, serializer):
        user = self.request.user
        
        if user.is_staff:
            serializer.save()
        else:
            raise DRFValidationError({"error": "Создание цены доступно только администратору."})

    def perform_update(self, serializer):
        user = self.request.user

        if user.is_staff:
            serializer.save()
        else:
            raise DRFValidationError({"error": "Редактирование цены доступно только администратору."})

    def perform_destroy(self, instance):
        user = self.request.user

        if user.is_staff:
            instance.delete()
        else:
            raise DRFValidationError({"error": "Удаление цены доступно только администратору."})

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        user = self.request.user
        
        if user.is_staff:
            serializer.save()
        else:
            raise DRFValidationError({"error": "Создание должности доступно только администратору."})

    def perform_update(self, serializer):
        user = self.request.user

        if user.is_staff:
            serializer.save()
        else:
            raise DRFValidationError({"error": "Редактирование должности доступно только администратору."})

    def perform_destroy(self, instance):
        user = self.request.user

        if user.is_staff:
            instance.delete()
        else:
            raise DRFValidationError({"error": "Удаление должности доступно только администратору."})

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        
        if user.is_staff:
            serializer.save()
        else:
            raise DRFValidationError({"error": "Создание сотрудника доступно только администратору."})

    def perform_update(self, serializer):
        user = self.request.user

        if user.is_staff:
            serializer.save()
        else:
            raise DRFValidationError({"error": "Редактирование сотрудника доступно только администратору."})

    def perform_destroy(self, instance):
        user = self.request.user

        if user.is_staff:
            instance.delete()
        else:
            raise DRFValidationError({"error": "Удаление сотрудника доступно только администратору."})

class PositionEmployeeViewSet(viewsets.ModelViewSet):
    queryset = PositionEmployee.objects.all()
    serializer_class = PositionEmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # Запрос всех заказов
    serializer_class = OrderSerializer  # Сериализатор для заказов
    permission_classes = [IsAuthenticated]  # Требуется аутентификация

    def perform_create(self, serializer):
        # Получаем текущего аутентифицированного пользователя
        user = self.request.user

        if not user.is_staff:
            # Пытаемся найти клиента с таким же email, как у пользователя
            try:
                client = Client.objects.get(email=user.email)  # Ищем клиента по email
            except Client.DoesNotExist:
                raise DRFValidationError({"error": "У пользователя нет привязанного клиента."})
            # Сохраняем заказ с привязкой к найденному клиенту
            serializer.save(client=client)
        else:
            serializer.save()

    def get_queryset(self):
        # Получаем текущего аутентифицированного пользователя
        user = self.request.user

        # Если пользователь администратор, возвращаем все заказы
        if user.is_staff:
            return Order.objects.all()

        # Ищем клиента по email пользователя
        try:
            client = Client.objects.get(email=user.email)
        except Client.DoesNotExist:
            # Если клиента не найдено, возвращаем пустой запрос
            return Order.objects.none()

        # Если у пользователя есть клиент, возвращаем только заказы этого клиента
        return Order.objects.filter(client=client)
    
    def perform_update(self, serializer):
        """Админ может редактировать любые заказы, клиент — нет."""
        user = self.request.user

        if user.is_staff:
            serializer.save()
        else:
            raise DRFValidationError({"error": "Редактирование заказа доступно только администратору."})

    def perform_destroy(self, instance):
        """Удалять заказы может только админ."""
        user = self.request.user

        if user.is_staff:
            instance.delete()
        else:
            raise DRFValidationError({"error": "Удаление заказа доступно только администратору."})

class PaymentOrderViewSet(viewsets.ModelViewSet):
    queryset = PaymentOrder.objects.all()
    serializer_class = PaymentOrderSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsClient]

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_staff:
            serializer.save()
            return

        # Получаем клиента, связанного с текущим пользователем
        try:
            client = Client.objects.get(email=user.email)
        except Client.DoesNotExist:
            raise DRFValidationError({"error": "У пользователя нет привязанного клиента."})

        # Получаем ID заказа из запроса
        order_id = self.request.data.get("order")
        if not order_id:
            raise DRFValidationError({"error": "Не указан order_id."})

        # Проверяем, существует ли такой заказ
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise DRFValidationError({"error": "Заказ не найден."})

        # Проверяем, принадлежит ли заказ текущему клиенту
        if order.client != client:
            raise DRFValidationError({"error": "Вы не можете создать платежное поручение для чужого заказа."})

        # Автоматически устанавливаем сумму платежа
        total_amount = order.total_cost

        # Создаём платежное поручение, передавая ID заказа
        serializer.save(client=client, order_id=order.id, total_amount=total_amount)

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return PaymentOrder.objects.all()

        try:
            client = Client.objects.get(email=user.email)
        except Client.DoesNotExist:
            return PaymentOrder.objects.none()

        return PaymentOrder.objects.filter(order__client=client)
    
    # Переопределяем метод для удаления
    def destroy(self, request, *args, **kwargs):
        # Только администратор может удалять поручения
        if not request.user.is_staff:
            raise DRFValidationError({"error": "Вы не можете удалить это поручение."})
        
        # Удаление поручения, если пользователь администратор
        return super().destroy(request, *args, **kwargs)

    # Переопределяем метод для редактирования
    def update(self, request, *args, **kwargs):
        # Только администратор может редактировать поручения
        if not request.user.is_staff:
            raise DRFValidationError({"error": "Вы не можете редактировать это поручение."})
        
        # Редактирование поручения, если пользователь администратор
        return super().update(request, *args, **kwargs)


# 1. Список выполненных работ
class CompletedOrdersListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return Order.objects.filter(status='completed').select_related('client', 'service', 'employee')

# 2. Список платежных поручений за период
class PaymentOrdersByPeriodView(generics.ListAPIView):
    serializer_class = PaymentOrderSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            try:
                start_date = parse_date(start_date)
                end_date = parse_date(end_date)
                if start_date > end_date:
                    raise DRFValidationError({"error": "Дата начала не может быть позже даты окончания."})
            except:
                raise DRFValidationError({"error": "Неверный формат даты. Используйте YYYY-MM-DD."})

            return PaymentOrder.objects.filter(payment_order_date__range=[start_date, end_date])
        return PaymentOrder.objects.all()

# 3. Просмотр номенклатуры рекламных услуг
class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsClient | IsAdmin]

    def get_queryset(self):
        """
        Переопределяем get_queryset, чтобы добавить связанные с услугами цены.
        """
        services = Service.objects.all()  # Получаем все услуги

        # Добавляем цены для каждой услуги
        for service in services:
            # Получаем цены для каждой услуги из PriceList
            service.prices = PriceList.objects.filter(service=service)  # Привязываем цены к каждой услуге

        return services

    def list(self, request, *args, **kwargs):
        """
        Переопределяем метод list, чтобы добавить цены в ответ.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Добавляем в ответ данные о ценах из связанного прайс-листа
        for i, service in enumerate(queryset):
            # Для каждой услуги добавляем цены в сериализованный ответ
            prices = PriceListSerializer(service.prices, many=True).data
            serializer.data[i]["prices"] = prices  # Включаем цены в ответ

        return Response(serializer.data)

# 4. Список заявок заказчика за период
class OrdersByClientView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    def get_queryset(self):
        # Получаем start_date, end_date и client_id из параметров запроса
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        client_id = self.request.query_params.get('client_id')

        # Если client_id не указан, администратор не сможет фильтровать по клиенту
        if not client_id:
            raise DRFValidationError({"error": "Не выбран клиент для фильтрации."})

        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            raise DRFValidationError({"error": "Клиент не найден."})

        # Если start_date и end_date заданы, фильтруем заявки по этим датам
        if start_date and end_date:
            try:
                start_date = parse_date(start_date)
                end_date = parse_date(end_date)
                if start_date > end_date:
                    raise DRFValidationError({"error": "Дата начала не может быть позже даты окончания."})
            except:
                raise DRFValidationError({"error": "Неверный формат даты. Используйте YYYY-MM-DD."})

            # Возвращаем заявки для выбранного клиента в указанном периоде
            return Order.objects.filter(client=client, order_date__range=[start_date, end_date])

        # Если даты не указаны, возвращаем все заявки для выбранного клиента
        return Order.objects.filter(client=client)

# 5. Список сотрудников с количеством выполненных заявок
class EmployeeOrdersCountView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        # Получаем параметры для фильтрации по датам
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        # Сначала фильтруем все заявки по датам и статусу
        filtered_orders = Order.objects.filter(
            status='completed',
            order_date__range=[start_date, end_date]
        )

        # Получаем всех сотрудников, которые связаны с этими заявками
        employees = Employee.objects.filter(order__in=filtered_orders).distinct()

        return employees

# 6. Отчет о стоимости работ за последний квартал
class QuarterlyReportView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, *args, **kwargs):
        last_quarter = now() - timedelta(days=90)
        report = Order.objects.filter(
            completion_date__gte=last_quarter, status="completed"
        ).aggregate(total_cost=Sum('total_cost'))
        return Response(report)