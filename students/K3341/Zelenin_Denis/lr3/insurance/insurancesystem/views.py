# views.py
from datetime import timedelta

from django.utils.timezone import now
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum, Q
from .models import (InsuranceAgent, Organization, Employee, CollectiveContract,
                      InsuranceCase, EmploymentContract)
from .serializers import (InsuranceAgentSerializer, OrganizationSerializer, EmployeeSerializer,
                          CollectiveContractSerializer,
                          InsuranceCaseSerializer, EmploymentContractSerializer)

class InsuranceAgentViewSet(viewsets.ModelViewSet):
    queryset = InsuranceAgent.objects.all()
    serializer_class = InsuranceAgentSerializer

    def create(self, request, *args, **kwargs):
        passport_details = request.data.get('passport_details')

        # Проверка, существует ли агент с такими паспортными данными
        agent, created = InsuranceAgent.objects.get_or_create(passport_details=passport_details, defaults=request.data)

        if created:
            message = 'New agent created.'
        else:
            message = 'Agent already exists.'

        # Создание нового контракта
        start_date = now().date()
        end_date = start_date + timedelta(days=365)
        new_contract = EmploymentContract.objects.create(
            insurance_agent=agent,
            start_date=start_date,
            end_date=end_date
        )

        contract_serializer = EmploymentContractSerializer(new_contract)

        return Response({
            'message': f'{message} New contract created.',
            'agent': self.get_serializer(agent).data,
            'contract': contract_serializer.data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
#####
    @action(detail=True, methods=['get'])
    def related_organizations(self, request, pk=None):
        organization = self.get_object()
        current_date = request.query_params.get('current_date')

        # Если current_date не указан, используем текущую дату
        if current_date is None:
            current_date = now().date()

        # Получаем агентов, связанных с заданной организацией через действующие договоры
        agent_ids = organization.collectivecontract_set.filter(
            end_date__gte=current_date
        ).values_list('insurance_agent_id', flat=True)

        # Находим другие организации, застрахованные теми же агентами
        related_orgs = Organization.objects.filter(
            collectivecontract__insurance_agent_id__in=agent_ids,
            collectivecontract__end_date__gte=current_date
        ).distinct().exclude(id=organization.id)

        serializer = self.get_serializer(related_orgs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])

    def contract_details_and_payouts(self, request, pk=None):
        organization = Organization.objects.get(pk=pk)
        contracts = CollectiveContract.objects.filter(organization=organization)

        # Сериализация контрактов
        serialized_contracts = CollectiveContractSerializer(contracts, many=True).data

        # Добавление общей суммы выплат к каждому контракту
        for contract_data, contract in zip(serialized_contracts, contracts):
            total_payout = contract.insurancecase_set.aggregate(total=Sum('payout_amount'))['total'] or 0
            contract_data['total_payout'] = total_payout

        return Response(serialized_contracts)
class CollectiveContractViewSet(viewsets.ModelViewSet):
    queryset = CollectiveContract.objects.all()
    serializer_class = CollectiveContractSerializer
#########
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Дата начала периода в формате YYYY-MM-DD",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="Дата окончания периода в формате YYYY-MM-DD",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def agent_contracts_count(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date:
            start_date = '1900-01-01'
        if not end_date:
            end_date = '2500-01-01'

        contracts = CollectiveContract.objects.filter(start_date__gte=start_date, end_date__lte=end_date)
        result = contracts.values('insurance_agent__full_name').annotate(
            collective_count=Count('id', filter=Q(organization__isnull=False)),
            individual_count=Count('id', filter=Q(organization__isnull=True))
        )
        return Response(result)

    @action(detail=True, methods=['get'])
    def insured_employees(self, request, pk=None):
        contract = self.get_object()
        employees = contract.employees.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)



class EmployeeCaseViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
class InsuranceCaseViewSet(viewsets.ModelViewSet):
    queryset = InsuranceCase.objects.all()
    serializer_class = InsuranceCaseSerializer
########
    @action(detail=False, methods=['get'])
    def total_payouts(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Установим значения по умолчанию, если параметры отсутствуют
        if not start_date:
            start_date = '1900-01-01'  # Далеко в прошлом, чтобы включить все возможные записи
        if not end_date:
            end_date = '2100-01-01'

        # Фильтруем страховые случаи по дате и суммируем выплаты по типам договоров
        cases = InsuranceCase.objects.filter(date__gte=start_date, date__lte=end_date)
        result = cases.values('contract__type').annotate(total_payout=Sum('payout_amount'))

        return Response(result)

class EmploymentContractViewSet(viewsets.ModelViewSet):
    queryset = EmploymentContract.objects.all()
    serializer_class = EmploymentContractSerializer
