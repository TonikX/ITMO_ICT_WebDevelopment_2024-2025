from rest_framework import viewsets
from .models import (
    InsuranceAgency, Agent, EmploymentContract, Organization,
    Employee, Position, Contract, InsuranceCase, CustomUser
)
from .serializers import (
    InsuranceAgencySerializer, AgentSerializer, EmploymentContractSerializer,
    OrganizationSerializer, EmployeeSerializer, PositionSerializer,
    ContractSerializer, InsuranceCaseSerializer
)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsAgent, IsOrganizationAdmin

class InsuranceAgencyViewSet(viewsets.ModelViewSet):
    queryset = InsuranceAgency.objects.all()
    serializer_class = InsuranceAgencySerializer


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer


class EmploymentContractViewSet(viewsets.ModelViewSet):
    queryset = EmploymentContract.objects.all()
    serializer_class = EmploymentContractSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class InsuranceCaseViewSet(viewsets.ModelViewSet):
    queryset = InsuranceCase.objects.all()
    serializer_class = InsuranceCaseSerializer


@receiver(post_save, sender=CustomUser)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'agent':
            group = Group.objects.get(name='Agent')
        elif instance.role == 'employee':
            group = Group.objects.get(name='Employee')
        elif instance.role == 'org_admin':
            group = Group.objects.get(name='Organization Admin')
        else:
            group = None

        if group:
            instance.groups.add(group)

class ContractListView(APIView):
    permission_classes = [IsAgent | IsOrganizationAdmin]

    def get(self, request):
        #TODO: Implement the logic to return the list of contracts
        return Response({'message': 'Access granted!'})