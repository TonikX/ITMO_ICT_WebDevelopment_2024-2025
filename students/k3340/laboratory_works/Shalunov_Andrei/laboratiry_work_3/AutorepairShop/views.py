from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils.timezone import now
from datetime import timedelta
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, F, ExpressionWrapper, DurationField
from rest_framework import viewsets
from .models import (
    User, Client, Employee, CarWorkshop,
    JobPosition, Automobile, Model, Contract,
    Service, Detail, CarDetail, DetailsFromClient,
    DistributionOfWork, DetailInService,
)
from .serializers import (
    ClientSerializer, EmployeeSerializer, CarWorkshopSerializer,
    JobPositionSerializer, AutomobileSerializer, ModelSerializer, ContractSerializer,
    ServiceSerializer, DetailSerializer, CarDetailSerializer, DetailsFromClientSerializer,
    DistributionOfWorkSerializer, DetailInServiceSerializer,
)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'phone', 'email']

    @swagger_auto_schema(
        method='get',
        operation_description="Получить данные, как часто клиент посещал автосервис за последний год",
        responses={
            200: openapi.Response(
                description="Информация о посещениях клиента",
                examples={
                    "application/json": {
                        "client": "Иван Иванов",
                        "visits": 5
                    }
                }
            )
        }
    )
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def yearly_visits(self, request, pk=None):
        client = self.get_object()
        last_year = now() - timedelta(days=365)
        visits = Contract.objects.filter(client=client, order_date__gte=last_year).count()
        return Response({'client': client.full_name, 'visits': visits})

    @swagger_auto_schema(
        method='get',
        operation_description="Получить владельцев автомобилей, которые обращались в ремонт больше одного раза",
        responses={
            200: openapi.Response(
                description="Информация о клиентах, которые обращались больше одного раза",
                examples={
                    "application/json": [
                        {"full_name": "Иван Иванов", "visits": 3},
                        {"full_name": "Петр Петров", "visits": 2}
                    ]
                }
            )
        }
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def repeat_clients(self, request):
        repeat_clients = (
            Client.objects.annotate(visits=Count('contract'))
            .filter(visits__gt=1)
            .values('full_name', 'visits')
        )
        return Response(repeat_clients)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'phone', 'email']


    @swagger_auto_schema(
        method='get',
        manual_parameters=[
            openapi.Parameter(
                'brand',
                openapi.IN_QUERY,
                description="Марка автомобиля",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def top_mechanic_by_brand(self, request):
        car_brand = request.query_params.get('brand')
        if not car_brand:
            return Response({'error': 'Parameter "brand" is required'}, status=400)

        mechanic = (
            Employee.objects.filter(
                contract__auto__auto_model__car_brand=car_brand,
                job_position__name__iexact="mechanic"
            )
            .annotate(job_count=Count('contract'))
            .order_by('-job_count')
            .first()
        )

        if mechanic:
            return Response({
                'car_brand': car_brand,
                'mechanic_name': mechanic.full_name,
                'job_counts': mechanic.job_count
            })
        return Response({'error': 'No mechanics found for this brand'})


    @swagger_auto_schema(
        method='get',
        responses={200: openapi.Response('Loyal clients', examples={"application/json": [{"client_name": "Иван Иванов"}]})}
    )
    #Владельцы авто, которых всегда обслуживает один механик
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def loyal_clients(self, request, pk=None):
        employee = self.get_object()

        if employee.job_position.name.lower() != "mechanic":
            return Response({'error': 'Этот сотрудник не является механиком'}, status=400)

        clients = Client.objects.filter(contract__employee=employee).distinct()
        loyal_clients = []

        for client in clients:
            mechanics = Contract.objects.filter(client=client).values('employee').distinct()
            if mechanics.count() == 1:
                loyal_clients.append({'client_name': client.full_name})

        return Response(loyal_clients)

    @swagger_auto_schema(
        method='get',
        responses={200: openapi.Response('Delayed days', examples={"application/json": [{"client_name": "Иван Иванов", "days_late": 5}]} )}
    )
    # Вывести количество дней просрочки выполнения для каждого заказа.
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def delayed_days(self, request, pk=None):
        employee = self.get_object()

        if employee.job_position.name.lower() != "mechanic":
            return Response({'error': 'Этот сотрудник не является механиком'}, status=400)

        delayed_jobs = (
            Contract.objects.filter(
                employee=employee,
                actual_date_end_of_repair__gt=F('scheduled_date_end_of_repair')
            )
            .annotate(
                days_late=ExpressionWrapper(
                    F('actual_date_end_of_repair') - F('scheduled_date_end_of_repair'),
                    output_field=DurationField()
                )
            )
            .values('client__full_name', 'days_late')
        )

        results = [
            {
                'client_name': job['client__full_name'],
                'days_late': job['days_late'].days
            }
            for job in delayed_jobs
        ]

        if not results:
            return Response({'message': 'Просроченных заказов нет.'})

        return Response(results)

    @swagger_auto_schema(
        method='get',
        responses={200: openapi.Response('Fines', examples={"application/json": [{"client_name": "Иван Иванов", "days_late": 3, "fine": 750.0}]})}
    )
    #Штраф для определенного механика за каждый день просрочки выполнения заказа за прошедший месяц
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def fines(self, request, pk=None):
        employee = self.get_object()

        if employee.job_position.name.lower() != "mechanic":
            return Response({'error': 'Этот сотрудник не является механиком'}, status=400)

        last_month = now() - timedelta(days=30)
        delayed_jobs = Contract.objects.filter(
            employee=employee,
            actual_date_end_of_repair__gt=F('scheduled_date_end_of_repair'),
            date_of_acceptance_for_repair__gte=last_month
        )

        results = []
        for job in delayed_jobs:
            days_late = (job.actual_date_end_of_repair - job.scheduled_date_end_of_repair).days
            fine = job.total_payment * 0.05 * days_late if job.total_payment else 0
            results.append({
                'client_name': job.client.full_name,
                'days_late': days_late,
                'fine': round(fine, 2)
            })

        if not results:
            return Response({'message': 'Нет просроченных заказов за последний месяц.'})

        return Response(results)

    @swagger_auto_schema(
        method='get',
        responses={200: openapi.Response('Monthly earnings', examples={"application/json": {"mechanic_name": "Иван Иванов", "total_earnings_last_month": 50000}})}
    )
    #Сколько заработал определенный мастер за прошедший месяц?
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def monthly_earnings(self, request, pk=None):
        employee = self.get_object()

        if employee.job_position.name.lower() != "mechanic":
            return Response({'error': 'Этот сотрудник не является механиком'}, status=400)

        last_month = now() - timedelta(days=30)
        earnings = (
            Contract.objects.filter(employee=employee, order_date__gte=last_month)
            .aggregate(total_earnings=Sum('total_payment'))
        )

        total_earnings = earnings['total_earnings'] or 0

        return Response({
            'mechanic_name': employee.full_name,
            'total_earnings_last_month': total_earnings
        })


class CarWorkshopViewSet(viewsets.ModelViewSet):
    queryset = CarWorkshop.objects.all()
    serializer_class = CarWorkshopSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['address', 'city']


class JobPositionViewSet(viewsets.ModelViewSet):
    queryset = JobPosition.objects.all()
    serializer_class = JobPositionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'specialisation']


class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['car_brand', 'model', 'car_power']


class AutomobileViewSet(viewsets.ModelViewSet):
    queryset = Automobile.objects.all()
    serializer_class = AutomobileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['engine_number', 'state_number', 'colour']


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['order_status', 'payment_status']


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['type_of_repair', 'category_repair']


class DetailViewSet(viewsets.ModelViewSet):
    queryset = Detail.objects.all()
    serializer_class = DetailSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'country_of_manufacturer']


class CarDetailViewSet(viewsets.ModelViewSet):
    queryset = CarDetail.objects.all()
    serializer_class = CarDetailSerializer
    permission_classes = [IsAuthenticated]


class DetailsFromClientViewSet(viewsets.ModelViewSet):
    queryset = DetailsFromClient.objects.all()
    serializer_class = DetailsFromClientSerializer
    permission_classes = [IsAuthenticated]


class DistributionOfWorkViewSet(viewsets.ModelViewSet):
    queryset = DistributionOfWork.objects.all()
    serializer_class = DistributionOfWorkSerializer
    permission_classes = [IsAuthenticated]


class DetailInServiceViewSet(viewsets.ModelViewSet):
    queryset = DetailInService.objects.all()
    serializer_class = DetailInServiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['detail__name', 'contract__id', 'number_of_details']