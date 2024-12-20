from django.db import models
from django.db.models import Count, Sum
from djoser.serializers import UserSerializer
from rest_framework import viewsets, views, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import (AgentSerializer, EmploymentContractSerializer,
                          OrganizationSerializer, EmployeeSerializer, ContractSerializer, InsuranceCaseSerializer,
                          CustomUserSerializer, InsuranceAgencySerializer)

from .models import (Agent, EmploymentContract, Organization, Employee,
                     Contract, InsuranceCase, CustomUser, InsuranceAgency)


@permission_classes([AllowAny])
class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

    @action(detail=True, methods=['get'])
    def contract_stats(self, request, pk=None):
        agent = self.get_object() # get agent by id
        contracts = EmploymentContract.objects.filter(agent=agent)
        total_contracts = contracts.count()
        total_salary = contracts.aggregate(total_salary=models.Sum('salary'))['total_salary']
        return Response({
            'agent_id': agent.id,
            'total_contracts': total_contracts,
            'total_salary': total_salary
        })

    @action(detail=False, methods=['get'])
    def contracts_count_by_date(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if not start_date or not end_date:
            return Response({"error": "start_date and end_date are required"}, status=400)

        contracts_count = Contract.objects.filter(
            start_date__gte=start_date,
            end_date__lte=end_date
        ).values('agent', 'contract_type').annotate(count=Count('id'))
        return Response(contracts_count)

    @action(detail=False, methods=['post'])
    def create_agent(self, request):
        serializer = AgentSerializer(data=request.data)
        if serializer.is_valid():
            agent = serializer.save()
            return Response(AgentSerializer(agent).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_agent(self, request, pk=None):
        agent = self.get_object()
        serializer = AgentSerializer(agent, data=request.data)
        if serializer.is_valid():
            agent = serializer.save()
            return Response(AgentSerializer(agent).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_agent(self, request, pk=None):
        agent = self.get_object()
        agent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([AllowAny])
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


@permission_classes([AllowAny])
class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    @action(detail=False, methods=['get'])
    def insurance_case_summary(self, request):
        insurance_cases = InsuranceCase.objects.all()
        total_payout_by_contract_type = insurance_cases.values('contract_type').annotate(
            total_payout=models.Sum('payout_amount')
        )
        return Response(total_payout_by_contract_type)

    @action(detail=False, methods=['get'])
    def active_contracts_report(self, request):
        report = Contract.objects.filter(end_date__isnull=False).values(
            'agent__id',
            'agent__first_name',
            'agent__last_name',
            'contract_type'
        ).annotate(
            count=Count('id'),
            total_sum=Sum('total_sum')
        )
        return Response(report)

    @action(detail=False, methods=['get'])
    def view_active_contracts(self, request):
        active_contracts_response = self.active_contracts_report(request)
        return Response({
            'message': 'Active contracts report',
            'data': active_contracts_response.data
        })


@permission_classes([AllowAny])
class InsuranceCaseViewSet(viewsets.ModelViewSet):
    queryset = InsuranceCase.objects.all()
    serializer_class = InsuranceCaseSerializer

    @action(detail=False, methods=['get'])
    def payout_summary(self, request):
        total_payout_by_type = InsuranceCase.objects.values('contract__contract_type').annotate(
            total_payout=models.Sum('payout_amount')
        )
        return Response(total_payout_by_type)


@permission_classes([AllowAny])
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=True, methods=['get'])
    def insured_employees(self, request, pk=None):
        employee = self.get_object()
        active_contracts = employee.contracts.filter(end_date__gte=models.F('start_date'))
        serializer = EmployeeSerializer(active_contracts, many=True)
        return Response(serializer.data)


@permission_classes([AllowAny])
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_user(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RelatedOrganizationsView(views.APIView):
    def get(self, request, organization_id):
        agents = Agent.objects.filter(contract__organization_id=organization_id,
                                      contract__end_date__isnull=True).distinct()
        related_organizations = Organization.objects.filter(
            contract__agent__in=agents,
            contract__end_date__isnull=True
        ).exclude(id=organization_id).distinct()
        serializer = OrganizationSerializer(related_organizations, many=True)
        return Response(serializer.data)


class ContractsCountByTypeView(views.APIView):
    def get(self, request, start_date, end_date):
        contracts_count = Contract.objects.filter(
            start_date__gte=start_date,
            end_date__lte=end_date
        ).values('agent', 'contract_type').annotate(count=Count('id'))
        return Response(contracts_count)

@permission_classes([AllowAny])
class InsuredEmployeesView(views.APIView):
    def get(self, request, person_id):
        contracts = Contract.objects.filter(
            agent__id=person_id
        )
        insured_employees = Employee.objects.filter(contract__in=contracts).distinct()
        serializer = EmployeeSerializer(insured_employees, many=True)
        return Response(serializer.data)


@permission_classes([AllowAny])
class TotalPayoutsByContractTypeView(views.APIView):
    def get(self, request, start_date, end_date):
        payouts = InsuranceCase.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).values('contract__contract_type').annotate(total_payout=Sum('payout_amount'))
        return Response(payouts)


class ContractDetailsAndTotalPayoutsView(views.APIView):
    def get(self, request):
        contract_details = Contract.objects.values(
            'organization__full_name',
            'id',
            'start_date',
            'end_date',
            'total_sum'
        ).annotate(total_payout=Sum('insurancecase__payout_amount'))
        return Response(contract_details)


class EmployeeContractViewSet(viewsets.ModelViewSet):
    queryset = EmploymentContract.objects.all()
    serializer_class = EmploymentContractSerializer
